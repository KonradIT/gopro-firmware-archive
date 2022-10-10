import lib
from utils import get_day, replace_line
import sys
import logging
import upload
from os.path import exists
from labs import LabsFirmwareDownloader

if __name__ == "__main__":

    logging.basicConfig(stream=sys.stdout, filemode="w", level=logging.INFO)

    logger = logging.getLogger()
    gopro = lib.FirmwareCatalog()
    uploader = upload.Upload()

    skip_cameras = ["CYT.01", "BCK.01", "SEN.01", "SLB.01", "SLS.01"]
    # Hydrate catalog entries
    gopro.get_catalog()
    logger.info(">> date: %s", get_day())
    for camera in gopro.get_all_cameras():

        if camera.ModelString in skip_cameras:
            continue
        logger.info(
            ":: camera: [%s] :: model: [%s] :: fw release date: [%s]"
            % (camera.Name, camera.ModelString, camera.ReleaseDate)
        )
        catalog_path = "./data/%s.md" % camera.get_safe_name()
        if not exists(catalog_path):
            with open(catalog_path, "w") as f:
                f.write(
                    "# 📷 Firmware archives for %s (%s):\n\n\n"
                    % (camera.Name, camera.ModelString)
                )
            with open("README.md", "a") as readme:
                readme.write("\n- [%s](%s)" % (camera.Name, catalog_path))
        if camera.ReleaseDate == get_day() or camera.ReleaseDate == get_day(1):
            logger.info(
                ">> new firmware released for camera %s (%s)"
                % (camera.Name, camera.ReleaseDate)
            )
            # upload to internet
            r = uploader.upload(
                file=camera.get_as_upload_payload(),
                file_len=camera.get_firmware_size(),
                version=camera.Version,
                release_notes=camera.ReleaseNotes,
                model_string=camera.ModelString,
                name=camera.Name,
                release_date=camera.ReleaseDate,
            )

            # prepare entry to repo catalog

            replace_line(
                catalog_path,
                1,
                """
- **%s** - Date: *%s*:
	- **Original Firmware URL**: %s
	- **Archive backup on GitHub repo**: %s
	- **Release Notes**:
            %s
"""
                % (
                    camera.Version,
                    camera.ReleaseDate,
                    camera.DownloadURL,
                    uploader.get_public_url(r),
                    camera.ReleaseNotes.replace("\n", "\n\t\t\t"),
                ),
            )

    l = LabsFirmwareDownloader()
    l.get()