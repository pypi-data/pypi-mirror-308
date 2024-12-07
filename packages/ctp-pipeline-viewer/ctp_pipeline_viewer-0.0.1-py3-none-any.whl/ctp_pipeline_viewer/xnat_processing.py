from typing import cast

from xnat import XNATSession

from src.ctp_pipeline_viewer.data_types import XnatExperimentInfo, View


def xnat_experiment_info(session: XNATSession, projects: list[tuple[str, list[View]]]) -> dict[str, XnatExperimentInfo]:
    """ Get a set of sessions in the pre-archive matching the project name. """
    result: dict[str, XnatExperimentInfo] = {}
    for project, views in projects:
        info = XnatExperimentInfo()
        if View.ARCHIVE in views:
            info.archive = {x.label for _, x in session.projects[project].experiments.items()}

        if View.PRE_ARCHIVE in views:
            info.pre_archive = {session.data['folderName'] for session in session.prearchive.sessions() if
                                session.project == project}

        result[project] = info

    return cast(dict[str, XnatExperimentInfo], dict(result))
