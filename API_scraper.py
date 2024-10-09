import logging
from app.sdk.models import KernelPlancksterSourceData, BaseJobState
from app.sdk.scraped_data_repository import ScrapedDataRepository
from app.setup import setup
from app.weather_API import scrape



def main(
    job_id: int,
    tracer_id: str,
    latitude:str,
    longitude:str,
    end_date: str,
    start_date:str,
    file_dir: str,
    kp_host: str,
    kp_port: str,
    kp_auth_token: str,
    kp_scheme: str,
    log_level: str = "WARNING"
) -> None:

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=log_level)

  
    if not all([job_id, tracer_id, latitude, longitude, start_date, end_date]):
        logger.error(f"{job_id}: job_id, tracer_id, coordinates, and date range must all be set.") 
        raise ValueError("job_id, tracer_id, coordinates, and date range must all be set.")


    kernel_planckster, protocol, file_repository = setup(
        job_id=job_id,
        logger=logger,
        kp_auth_token=kp_auth_token,
        kp_host=kp_host,
        kp_port=kp_port,
        kp_scheme=kp_scheme,
    )

    scraped_data_repository = ScrapedDataRepository(
        protocol=protocol,
        kernel_planckster=kernel_planckster,
        file_repository=file_repository,
    )



    scrape(
        job_id=job_id,
        tracer_id=tracer_id,
        scraped_data_repository=scraped_data_repository,
        log_level=log_level,
        latitude=latitude,
        longitude=longitude,  
        start_date=start_date,
        end_date=end_date,
        file_dir=file_dir
    )



if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(description="Scrape data from Sentinel datacollection.")


    parser.add_argument(
        "--job-id",
        type=str,
        default="1",
        help="The job id",
    )

    parser.add_argument(
        "--tracer-id",
        type=str,
        default="1",
        help="The tracer id",
    )

    parser.add_argument(
        "--log-level",
        type=str,
        default="WARNING",
        help="The log level to use when running the scraper. Possible values are DEBUG, INFO, WARNING, ERROR, CRITICAL. Set to WARNING by default.",
    )

    parser.add_argument(
        "--latitude",
        type=str,
        default="0",
        required=True,
        help="latitude of the location",
    )

    parser.add_argument(
        "--longitude",
        type=str,
        default="0",
        required=True,
        help="longitude of the location",
    )

    parser.add_argument(
        "--start_date",
        type=str,
        default="2023-08-08",
        required=True,
        help="start date",
    )

    parser.add_argument(
        "--end_date",
        type=str,
        default="2023-08-30",
        required=True,
        help="end date",
    )

    parser.add_argument(
        "--kp_host",
        type=str,
        default="60",
        help="kp host",
    )

    parser.add_argument(
        "--kp_port",
        type=int,
        default="60",
        help="kp port",
    )

    parser.add_argument(
        "--kp_auth_token",
        type=str,
        default="60",
        help="kp auth token",
        )

    parser.add_argument(
        "--kp_scheme",
        type=str,
        default="http",
        help="kp scheme",
        )

    parser.add_argument(
        "--file_dir",
        type=str,
        default="./.tmp",
        help="saved file directory",
    )




    args = parser.parse_args()


    main(
        job_id=args.job_id,
        tracer_id=args.tracer_id,
        log_level=args.log_level,
        latitude=args.latitude,
        longitude=args.longitude,
        start_date=args.start_date,
        end_date=args.end_date,
        kp_host=args.kp_host,
        kp_port=args.kp_port,
        kp_auth_token=args.kp_auth_token,
        kp_scheme=args.kp_scheme,
        file_dir=args.file_dir
    )

