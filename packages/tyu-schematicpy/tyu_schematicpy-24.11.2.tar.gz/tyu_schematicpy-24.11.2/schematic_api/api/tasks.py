import os
from flask import send_from_directory

from celery import shared_task


from schematic.manifest.generator import ManifestGenerator
from schematic.utils.schema_utils import (
    DisplayLabelType,
)


@shared_task(bind=True)
def get_manifest_task(
    self,
    schema_url: str,
    use_annotations: bool,
    dataset_id=None,
    asset_view=None,
    output_format=None,
    title=None,
    strict_validation: bool = True,
    data_model_labels: DisplayLabelType = "class_label",
    data_type: str = None,
    access_token: str = None,
):
    """Get the immediate dependencies that are related to a given source node.
    Args:
        schema_url: link to data model in json ld or csv format
        title: title of a given manifest.
        dataset_id: Synapse ID of the "dataset" entity on Synapse (for a given center/project).
        data_type: data model components.
        output_format: contains three option: "excel", "google_sheet", and "dataframe". if set to "excel", return an excel spreadsheet
        use_annotations: Whether to use existing annotations during manifest generation
        asset_view: ID of view listing all project data assets. For example, for Synapse this would be the Synapse ID of the fileview listing all data assets for a given project.
        strict: bool, strictness with which to apply validation rules to google sheets.
    Returns:
        Googlesheet URL (if sheet_url is True), or pandas dataframe (if sheet_url is False).
    """

    #
    all_results = ManifestGenerator.create_manifests(
        path_to_data_model=schema_url,
        output_format=output_format,
        data_types=data_type,
        title=title,
        access_token=access_token,
        dataset_ids=dataset_id,
        strict=strict_validation,
        use_annotations=use_annotations,
        data_model_labels=data_model_labels,
    )
    self.update_state(
        state="PROGRESS", meta={"current": 1, "total": 4, "status": "created manifest"}
    )
    # return an excel file if output_format is set to "excel"
    if output_format == "excel":
        # should only contain one excel spreadsheet path
        if len(all_results) > 0:
            result = all_results[0]
            dir_name = os.path.dirname(result)
            file_name = os.path.basename(result)
            mimetype = (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            return send_from_directory(
                directory=dir_name,
                path=file_name,
                as_attachment=True,
                mimetype=mimetype,
                max_age=0,
            )
    self.update_state(
        state="PROGRESS", meta={"current": 1, "total": 4, "status": "created manifest"}
    )
    return {
        "current": 100,
        "total": 100,
        "status": "Task completed!",
        "result": all_results,
    }
