from typing import List
from logging import getLogger
from datetime import datetime
import asyncio
from sd_alert_pipe.lasair import LasairService
from sd_alert_pipe.lasair import DATETIME_FORMAT as LASAIR_DT_FORMAT
from sd_alert_pipe.common import RootResult, gather_data

from app.config import settings
from app.targets.models import Target, Detection
from app.targets.schema import TargetCreate, TargetUpdate
from app.targets.crud import update_target, create_target

logger = getLogger(__name__)


async def ingest() -> int:
    num_saved = 0
    ls = LasairService()
    results = await ls.stored_query(settings.LASAIR_STORED_QUERY)

    if not results.get('last_entry'):
        print(results)
        logger.error('Could not determine Lasair\'s latest entry. Aborting')
        return 0

    latest_entry = datetime.strptime(results['last_entry'], LASAIR_DT_FORMAT)
    logger.info(f'Latest entry is from {latest_entry}')
    # If there are no targets with a timestamp greater than the latest entry,
    # we'll search for new targets.
    new_entries = not await Target.exists().where(Target.utc >= latest_entry).run()
    if new_entries:
        latest = latest_times(results['digest'])
        objectids = await names_to_query(latest)
        # we need to cut this short for now
        objectids = objectids[:3]
        targets = await create_or_update_names(objectids)
        for target in targets:
            await update_mags(target)
            target.utc = latest[target.name]
            await target.save()
        num_saved = len(targets)

    return num_saved


def latest_times(results: List[dict]) -> dict[str, datetime]:
    """
    Associate each name in the lasair result with the latest UTC
    timestamp it has
    """
    # Get a list of ObjectIds and associated UTC times
    name_times = [(r['objectId'], datetime.strptime(r['UTC'], LASAIR_DT_FORMAT)) for r in results]

    # Assocate the objectID with the latest timestamp
    latest_times = {}
    for (name, time) in name_times:
        if not latest_times.get(name):
            latest_times[name] = time
        elif latest_times.get(name) < time:
            latest_times[name] = time
        else:
            pass

    return latest_times


async def names_to_query(latest_times: dict[str, datetime]) -> List[str]:
    """
    Given an association of name and latest timestamp, we need to query
    the database to see if any of the names need to be updated or created.
    Returns a list of names that do.
    """
    names_to_query = []
    for name, time in latest_times.items():
        if not await Target.exists().where((Target.name == name) & (Target.utc >= time)).run():
            names_to_query.append(name)

    return names_to_query


async def create_or_update_names(objectids: List[str]) -> List[Target]:
    """
    Gather data for each name we want to fetch, then either update exsiting targets
    or create new ones
    """
    gathered_data = await asyncio.gather(*[gather_data(objectid) for objectid in objectids])
    if not all([all([result.lasair, result.mars]) for result in gathered_data]):
        logger.error('Missing data in results, aborting')
        return []

    targets = await asyncio.gather(*[rootresult_to_target(result) for result in gathered_data])
    return targets


async def rootresult_to_target(result: RootResult) -> Target:
    if await Target.exists().where(Target.name == result.name).run():
        target = await Target.objects().where(Target.name == result.name).first().run()
        target_update = TargetUpdate(
            id=target.id,
            classification=result.lasair.classification['type'],
            ra=result.common.ra,
            dec=result.common.dec,
        )
        target = await update_target(target_update)
    else:
        target_create = TargetCreate(
            name=result.name,
            classification=result.lasair.classification['type'],
            ra=result.common.ra,
            dec=result.common.dec,
            utc=datetime.fromtimestamp(0)
        )
        target = await create_target(target_create)

    await update_lightcurve(target, result.mars.data['prv_candidate'])
    return target


async def update_lightcurve(target: Target, lightcurve: list) -> List[Detection]:
    detections: List[Detection] = []
    for c in lightcurve:
        if not c.get('candid'):
            # Non detection
            continue
        if not await Detection.exists().where(Detection.candid == c['candid']).run():
            candidate = c['candidate']
            detection: Detection = Detection(
                target=target.id,
                candid=c['candid'],
                filter=candidate['filter'],
                magpsf=candidate['magpsf'],
                sigmapsf=candidate['sigmapsf'],
                diffmaglim=candidate['diffmaglim'],
                isdiffpos=candidate['isdiffpos'],
                jd=candidate['jd'],
                utc=datetime.strptime(candidate['wall_time'], '%a, %d %b %Y %H:%M:%S %Z'),
            )
            detections.append(detection)

    if len(detections) > 0:
        await Detection.insert(*detections).run()

    return detections


async def update_mags(target: Target) -> Target:
    latest_r_mag = await Detection.select('magpsf').where(
        (Detection.target == target.id) &
        (Detection.filter == 'r')
    ).order_by('utc', ascending=False).limit(1).run()
    latest_g_mag = await Detection.select('magpsf').where(
        (Detection.target == target.id) &
        (Detection.filter == 'g')
    ).order_by('utc', ascending=False).limit(1).run()
    max_r_mag = await Detection.select('magpsf').where(
        (Detection.target == target.id) &
        (Detection.filter == 'r')
    ).order_by('magpsf', ascending=True).limit(1).run()
    max_g_mag = await Detection.select('magpsf').where(
        (Detection.target == target.id) &
        (Detection.filter == 'g')
    ).order_by('magpsf', ascending=True).limit(1).run()
    target.latest_r_mag = latest_r_mag[0]['magpsf']
    target.latest_g_mag = latest_g_mag[0]['magpsf']
    target.max_g_mag = max_g_mag[0]['magpsf']
    target.max_r_mag = max_r_mag[0]['magpsf']
    await target.save().run()

    return target
