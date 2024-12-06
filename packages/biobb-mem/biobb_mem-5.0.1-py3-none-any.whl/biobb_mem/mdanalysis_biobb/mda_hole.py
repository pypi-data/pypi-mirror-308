#!/usr/bin/env python3

"""Module containing the Cpptraj Density class and the command line interface."""
import argparse
from biobb_common.generic.biobb_object import BiobbObject
from biobb_common.configuration import settings
from biobb_common.tools.file_utils import launchlogger
import MDAnalysis as mda
from MDAnalysis.analysis import hole2


class MDAHole(BiobbObject):
    """
    | biobb_mem MDAHole
    | Wrapper of the MDAnalysis HOLE module for analyzing ion channel pores or transporter pathways.
    | MDAnalysis HOLE provides an interface to the HOLE suite of tools to analyze pore dimensions and properties along a channel or transporter pathway. The parameter names and defaults follow the `MDAnalysis HOLE<https://docs.mdanalysis.org/stable/documentation_pages/analysis/hole2.html>`_  implementation.

    Args:
        input_top_path (str): Path to the input structure or topology file. File type: input. `Sample file <https://github.com/bioexcel/biobb_mem/raw/master/biobb_mem/test/data/A01JD/A01JD.pdb>`_. Accepted formats: crd (edam:3878), gro (edam:2033), mdcrd (edam:3878), mol2 (edam:3816), pdb (edam:1476), pdbqt (edam:1476), prmtop (edam:3881), psf (edam:3882), top (edam:3881), tpr (edam:2333), xml (edam:2332), xyz (edam:3887).
        input_traj_path (str): Path to the input trajectory to be processed. File type: input. `Sample file <https://github.com/bioexcel/biobb_mem/raw/master/biobb_mem/test/data/A01JD/A01JD.xtc>`_. Accepted formats: arc (edam:2333), crd (edam:3878), dcd (edam:3878), ent (edam:1476), gro (edam:2033), inpcrd (edam:3878), mdcrd (edam:3878), mol2 (edam:3816), nc (edam:3650), pdb (edam:1476), pdbqt (edam:1476), restrt (edam:3886), tng (edam:3876), trr (edam:3910), xtc (edam:3875), xyz (edam:3887).
        output_hole_path (str): Path to the output HOLE analysis results. File type: output. Accepted formats: vmd (edam:format_2330).
        properties (dic - Python dictionary object containing the tool parameters, not input/output files):
            * **start** (*int*) - (None) Starting frame for slicing.
            * **stop** (*int*) - (None) Ending frame for slicing.
            * **steps** (*int*) - (None) Step for slicing.
            * **executable** (*str*) - ("hole") Path to the HOLE executable.
            * **select** (*str*) - ("protein") The selection string to create an atom selection that the HOLE analysis is applied to.
            * **cpoint** (*list*) - (None) Coordinates of a point inside the pore (Å). If None, tries to guess based on the geometry.
            * **cvect** (*list*) - (None) Search direction vector. If None, tries to guess based on the geometry.
            * **sample** (*int*) - (0.2) Distance of sample points in Å. This value determines how many points in the pore profile are calculated.
            * **end_radius** (*float*) - (22) Radius in Å, which is considered to be the end of the pore.
            * **dot_density** (*int*) - (15) [5~35] Density of facets for generating a 3D pore representation.
            * **remove_tmp** (*bool*) - (True) [WF property] Remove temporal files.
            * **restart** (*bool*) - (False) [WF property] Do not execute if output files exist.
            * **sandbox_path** (*str*) - ("./") [WF property] Parent path to the sandbox directory.

    Examples:
        This is a use example of how to use the building block from Python::

            from biobb_mem.mdanalysis_biobb.mda_hole import mda_hole
            prop = {
                'select': 'protein',
                'executable': 'hole'
            }
            mda_hole(input_top_path='/path/to/myTopology.pdb',
                    input_traj_path='/path/to/myTrajectory.xtc',
                    output_hole_path='/path/to/hole_analysis.csv',
                    properties=prop)

    Info:
        * wrapped_software:
            * name: MDAnalysis
            * version: 2.7.0
            * license: GNU
        * ontology:
            * name: EDAM
            * schema: http://edamontology.org/EDAM.owl
    """

    def __init__(self, input_top_path, input_traj_path, output_hole_path,
                 properties=None, **kwargs) -> None:
        properties = properties or {}

        # Call parent class constructor
        super().__init__(properties)
        self.locals_var_dict = locals().copy()

        # Input/Output files
        self.io_dict = {
            "in": {"input_top_path": input_top_path, "input_traj_path": input_traj_path},
            "out": {"output_hole_path": output_hole_path}
        }

        # Properties specific for MDAHole
        self.start = properties.get('start', None)
        self.stop = properties.get('stop', None)
        self.steps = properties.get('steps', None)
        self.executable = properties.get('executable', 'hole')
        self.select = properties.get('select', 'protein')
        self.cpoint = properties.get('cpoint', None)
        self.cvect = properties.get('cvect', None)
        self.sample = properties.get('sample', 0.2)
        self.end_radius = properties.get('end_radius', 22)
        self.dot_density = properties.get('dot_density', 15)
        self.properties = properties

        # Check the properties
        self.check_properties(properties)
        self.check_arguments()

    @launchlogger
    def launch(self) -> int:
        """Execute the :class:`MDAHole <mdanalysis_biobb.mda_hole.MDAHole>` class."""

        # Setup Biobb
        if self.check_restart():
            return 0
        self.stage_files()

        # Load the universe
        u = mda.Universe(self.stage_io_dict["in"]["input_top_path"],
                         self.stage_io_dict["in"]["input_traj_path"])

        # Create HoleAnalysis object
        hole = hole2.HoleAnalysis(
            universe=u,
            select=self.select,
            cpoint=self.cpoint,
            cvect=self.cvect,
            sample=self.sample,
            executable=self.executable
        )
        # Run the analysis with step parameter
        hole.run(
            start=self.start,
            stop=self.stop,
            step=self.steps
        )
        hole.create_vmd_surface(
            self.stage_io_dict["out"]["output_hole_path"],
            dot_density=self.dot_density
        )
        hole.delete_temporary_files()
        # Copy files to host
        self.copy_to_host()
        # remove temporary folder(s)
        self.tmp_files.extend([
            self.stage_io_dict.get("unique_dir")
        ])
        self.remove_tmp_files()

        self.check_arguments(output_files_created=True, raise_exception=False)

        return self.return_code


def mda_hole(input_top_path: str, input_traj_path: str, output_hole_path: str = None, properties: dict = None, **kwargs) -> int:
    """Execute the :class:`MDAHole <mdanalysis_biobb.mda_hole.MDAHole>` class and
    execute the :meth:`launch() <mdanalysis_biobb.mda_hole.MDAHole.launch>` method."""

    return MDAHole(input_top_path=input_top_path,
                   input_traj_path=input_traj_path,
                   output_hole_path=output_hole_path,
                   properties=properties, **kwargs).launch()


def main():
    """Command line execution of this building block. Please check the command line documentation."""
    parser = argparse.ArgumentParser(description="Analyze ion channel pores or transporter pathways.", formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, width=99999))
    parser.add_argument('--config', required=False, help='Configuration file')

    # Specific args of each building block
    required_args = parser.add_argument_group('required arguments')
    required_args.add_argument('--input_top_path', required=True, help='Path to the input structure or topology file. Accepted formats: crd, gro, mdcrd, mol2, pdb, pdbqt, prmtop, psf, top, tpr, xml, xyz.')
    required_args.add_argument('--input_traj_path', required=True, help='Path to the input trajectory to be processed. Accepted formats: arc, crd, dcd, ent, gro, inpcrd, mdcrd, mol2, nc, pdb, pdbqt, restrt, tng, trr, xtc, xyz.')
    required_args.add_argument('--output_hole_path', required=True, help='Path to the output HOLE analysis results. Accepted formats: vmd.')

    args = parser.parse_args()
    args.config = args.config or "{}"
    properties = settings.ConfReader(config=args.config).get_prop_dic()

    # Specific call of each building block
    mda_hole(input_top_path=args.input_top_path,
             input_traj_path=args.input_traj_path,
             output_hole_path=args.output_hole_path,
             properties=properties)


if __name__ == '__main__':
    main()
