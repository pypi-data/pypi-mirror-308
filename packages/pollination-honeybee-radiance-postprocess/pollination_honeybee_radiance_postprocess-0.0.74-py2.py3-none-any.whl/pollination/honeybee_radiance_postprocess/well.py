from dataclasses import dataclass
from pollination_dsl.function import Function, command, Inputs, Outputs


@dataclass
class WellAnnualDaylight(Function):
    """Calculate credits for WELL L06 and L01."""

    folder = Inputs.folder(
        description='This folder is an output folder of annual daylight recipe. Folder '
        'should include grids_info.json and sun-up-hours.txt. The command uses the list '
        'in grids_info.json to find the result files for each sensor grid.',
        path='results'
    )

    grid_filter = Inputs.str(
        description='Text for a grid identifier or a pattern to filter the sensor grids '
        'of the model.',
        default='*'
    )

    model = Inputs.file(
        description='Path to HBJSON file. The purpose of the model in this function is '
        'to use the mesh area of the sensor grids to calculate area-weighted metrics. '
        'In case no model is provided or the sensor grids in the model do not have any '
        'mesh area, it will be assumed that all sensor points cover the same area.',
        path='model.hbjson', optional=True
    )

    @command
    def well_annual_daylight(self):
        return 'honeybee-radiance-postprocess post-process well well-annual-daylight ' \
            'results --use-states --sub-folder well_summary'

    # outputs
    l06_well_summary = Outputs.folder(
        description='WELL L06 summary folder. This folder includes all the other '
        'sub-folders which are also exposed as separate outputs.',
        path='l06_well_summary'
    )

    l01_well_summary = Outputs.folder(
        description='WELL L01 summary folder. This folder includes all the other '
        'sub-folders which are also exposed as separate outputs.',
        path='l01_well_summary'
    )
