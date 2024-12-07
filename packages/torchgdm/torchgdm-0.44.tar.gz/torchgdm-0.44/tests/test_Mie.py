# encoding=utf-8
# %%
import unittest
import warnings

import torch

import torchgdm as tg


class TestMie3D(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing Mie polarizabilities simulation...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # setup test cases
        self.test_cases = [
            dict(
                wl=700.0,
                radii=[80, 80],
                materials=[16, 16],
                eps_env=1.0,
            ),
            dict(
                wl=900.0,
                radii=[50, 70],
                materials=[12.0 + 0.1j, 9.0],
                eps_env=1.3**2,
            ),
            dict(
                wl=500.0,
                radii=[30, 30],
                materials=[-16.0959 + 0.4438j, -16.0959 + 0.4438j],
                eps_env=1.0,
            ),
            dict(
                wl=600.0,
                radii=[50, 70],
                materials=[-16.0959 + 0.4438j, 16],
                eps_env=1.0,
            ),
            dict(
                wl=650.0,
                radii=[70, 90],
                materials=[9.0, -16.0959 + 0.4438j],
                eps_env=1.5,
            ),
        ]

    def test_cross_sections(self):
        import numpy as np

        # try importing external packages
        try:
            # ignore import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                import pymiecs
        except ModuleNotFoundError:
            print(
                "Skipping test. Mie tests require package `pymiecs`. "
                + "Please install via `pip install pymiecs`."
            )
            return
        try:
            # ignore import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                import treams
            from torchgdm.tools.mie import mie_crosssections_sphere_3d, mie_crosssections_sphere_3d
        except ModuleNotFoundError:
            print(
                "Skipping test. Mie tests require package `treams`. "
                + "Please install via `pip install treams`."
            )
            return

        # - the actual test
        for device in self.devices:
            # ignore warnings temporarily:
            warnings.simplefilter("ignore")
            for conf in self.test_cases:
                wl = conf["wl"]
                k0 = 2 * np.pi / wl
                radii = conf["radii"]
                materials = conf["materials"]
                eps_env = conf["eps_env"]

                # torchGDM using treams-Mie
                env = tg.env.EnvHomogeneous3D(eps_env)
                struct_mie = tg.struct.StructMieSphereEffPola3D(
                    wavelengths=wl, environment=env, radii=radii, materials=materials
                )
                e_inc = tg.env.freespace_3d.PlaneWave()
                sim_tg_mie = tg.Simulation(
                    structures=struct_mie,
                    environment=env,
                    illumination_fields=e_inc,
                    wavelengths=wl,
                    device=device,
                )
                sim_tg_mie.run(verbose=False, progress_bar=False)
                cs_a_mie = sim_tg_mie.get_crosssections(progress_bar=False)

                # external Mie toolkit
                res_mie = pymiecs.main.Q(
                    tg.to_np(k0),
                    r_core=radii[0],
                    n_core=materials[0] ** 0.5,
                    r_shell=radii[1],
                    n_shell=materials[1] ** 0.5,
                    n_max=1,
                    n_env=tg.to_np(eps_env) ** 0.5,
                )
                ecs_mie = res_mie["cs_geo"] * res_mie["qext"]
                scs_mie = res_mie["cs_geo"] * res_mie["qsca"]

                # internal treams based Mie tool
                ecs_mie_treams = mie_crosssections_sphere_3d(
                    wavelengths=wl,
                    environment=env,
                    radii=radii,
                    materials=materials,
                    l_max=1,
                    device=device,
                )
                ecs_mie_treams = ecs_mie_treams["Cext"]

                # test if results match
                np.testing.assert_allclose(
                    ecs_mie[0], tg.to_np(ecs_mie_treams), atol=1e-2, rtol=1e-5
                )
                np.testing.assert_allclose(
                    ecs_mie[0], tg.to_np(cs_a_mie["ecs"][0]), atol=1e-2, rtol=1e-5
                )
                torch.testing.assert_close(
                    ecs_mie_treams, cs_a_mie["ecs"][0], atol=1, rtol=1e-4
                )

                # absorption and thus scattering are not accurate, increase tolerance
                np.testing.assert_allclose(
                    scs_mie[0], tg.to_np(cs_a_mie["scs"][0]), atol=1e-1, rtol=1e-2
                )

                if self.verbose:
                    print("  - {}: 3D Mie test passed.".format(device))


class TestMie(unittest.TestCase):

    def setUp(self):
        self.verbose = False
        if self.verbose:
            print("testing Mie polarizabilities simulation...")

        # --- determine if GPU is available
        self.devices = ["cpu"]
        if torch.cuda.is_available():
            self.devices.append("cuda:0")

        # setup test cases
        self.test_cases = [
            dict(
                wl=700.0,
                radii=[80, 80],
                materials=[16, 16],
                eps_env=1.0,
            ),
            dict(
                wl=900.0,
                radii=[50, 70],
                materials=[12.0 + 0.1j, 9.0],
                eps_env=1.3**2,
            ),
            dict(
                wl=500.0,
                radii=[30, 30],
                materials=[-16.0959 + 0.4438j, -16.0959 + 0.4438j],
                eps_env=1.0,
            ),
            dict(
                wl=600.0,
                radii=[50, 70],
                materials=[-16.0959 + 0.4438j, 16],
                eps_env=1.0,
            ),
            dict(
                wl=650.0,
                radii=[70, 90],
                materials=[9.0, -16.0959 + 0.4438j],
                eps_env=1.5,
            ),
        ]

    def test_cross_sections(self):
        import numpy as np

        # try importing external packages
        try:
            # ignore import warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                import treams
                from torchgdm.tools.mie import mie_crosssections_cylinder_2d
        except ModuleNotFoundError:
            return

        # - the actual test
        for device in self.devices:
            # ignore warnings temporarily:
            warnings.simplefilter("ignore")
            for i_case, conf in enumerate(self.test_cases):
                # print(i_case)
                
                wl = conf["wl"]
                k0 = 2 * np.pi / wl
                radii = conf["radii"]
                materials = conf["materials"]
                eps_env = conf["eps_env"]

                # internal treams based 2D Mie tool
                cs_mie_treams = mie_crosssections_cylinder_2d(
                    wavelengths=wl,
                    environment=eps_env,
                    radii=radii,
                    materials=materials,
                    m_max=2,
                    device=device,
                )
                ecs_mie_par = cs_mie_treams["Cext_par"]
                ecs_mie_perp = cs_mie_treams["Cext_perp"]
                scs_mie_par = cs_mie_treams["Csca_par"]
                scs_mie_perp = cs_mie_treams["Csca_perp"]

                # torchGDM using treams-Mie
                env = tg.env.EnvHomogeneous2D(eps_env)
                struct_mie = tg.struct.StructMieCylinderEffPola2D(
                    wavelengths=wl, environment=env, radii=radii, materials=materials
                )
                e_inc = [
                    tg.env.freespace_2d.PlaneWave(e0s=1, e0p=0),
                    tg.env.freespace_2d.PlaneWave(e0s=0, e0p=1),
                ]
                sim_tg_mie = tg.Simulation(
                    structures=struct_mie,
                    environment=env,
                    illumination_fields=e_inc,
                    wavelengths=wl,
                    device=device,
                )
                sim_tg_mie.run(verbose=False, progress_bar=False)
                cs_a_mie = sim_tg_mie.get_crosssections(progress_bar=False)

                # test if results match
                # print(ecs_mie_par, cs_a_mie["ecs"][:,0], eps_env)
                torch.testing.assert_close(
                    ecs_mie_par, cs_a_mie["ecs"][:,0], atol=1e-2, rtol=1e-5
                )
                torch.testing.assert_close(
                    ecs_mie_perp, cs_a_mie["ecs"][:,1], atol=1e-2, rtol=1e-5
                )
                torch.testing.assert_close(
                    scs_mie_par, cs_a_mie["scs"][:,0], atol=1e-2, rtol=1e-5
                )
                torch.testing.assert_close(
                    scs_mie_perp, cs_a_mie["scs"][:,1], atol=1e-2, rtol=1e-5
                )

                if self.verbose:
                    print("  - {}: 2D Mie test passed.".format(device))


# %%
if __name__ == "__main__":
    print("testing Mie polarizabilities...")
    torch.set_printoptions(precision=7)
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
