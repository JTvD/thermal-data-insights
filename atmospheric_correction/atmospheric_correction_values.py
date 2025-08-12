
import pandas as pd
import numpy as np
import math

# Implementation of the Passman Larmore Model from
# Atmospheric transmission coefficient modelling in the infrared for
# thermovision measurements (Minkina and Klecha, 2016)
# Based on Infrared Thermography (G. Gaussorgues, 1994) chapter 4.5:
# A PRACTICAL METHOD FOR CALCULATING ATMOSPHERIC TRANSMISSION


# Input: wavelength in um (micrometer) and distance in meters
# Output: Transmission due to scattering
def atmospheric_scattering(wavelength, distance):
    scattering_coefficient = 0.20 * (0.6 / wavelength) ** 1.3
    pscat = math.exp(-scattering_coefficient * (distance / 1000))
    print(f"wavelength: {wavelength}")
    print(f"scattering coefficient: {scattering_coefficient}")
    print(f"Transmission due to scattering: {pscat}")
    return pscat


class PassmanLarmoreModel:
    def __init__(self, vapout_table_filename=None, carbon_table_filename=None):
        if vapout_table_filename is None or carbon_table_filename is None:
            raise Exception(
                "The Passman Larmore model must be called with a vapout_table_filename "
                "and carbon_table_filename "
            )
        # load the lookup tables, dataframe for the index & header.
        # X axis is the h value Y axis is the wave length
        self.vapour_table = pd.read_csv(vapout_table_filename, dtype=float)
        self.h_aprox_vals_list = self.vapour_table.columns.values
        self.h_aprox_vals_np = np.asarray(
            self.h_aprox_vals_list, dtype=np.float64
        )
        # print(self.vapour_table)
        self.carbon_table = pd.read_csv(carbon_table_filename, dtype=float)
        # print(self.carbon_table)

    def atmospheric_transmission(self, tatm, humidity, distance, wavelength):
        """
        Calculate atmospheric transmission based on the Passman Larmore model.
        :param tatm: Ambient temperature in degrees Celsius
        :param humidity: Relative humidity (0 to 1)
        :param distance: Distance in meters
        :param wavelength: Wavelength in micrometers
        :return: Atmospheric transmission value
        """
        # Calculate the h value based on the temperature, humidity and distance
        h_exact = (
            1.6667e-4 * tatm ** 3 + 0.01 * tatm ** 2 + 0.38333 * tatm + 5
        ) * humidity * (distance / 1e3)
        # Get closest h value index from the table
        h_aprox_ind = (abs(self.h_aprox_vals_np - h_exact)).argmin()
        p_vapour = self.vapour_table.at[
            wavelength, self.h_aprox_vals_list[h_aprox_ind]
        ]
        # Carbon index is the closest value to the distance in km
        d_aprox_ind = (abs(self.h_aprox_vals_np - (distance / 1000))).argmin()
        p_carbon = self.carbon_table.at[
            wavelength, self.h_aprox_vals_list[d_aprox_ind]
        ]
        patm = p_vapour * p_carbon
        return patm

    def absorption_per_distance(
        self, ambient_temperature, relative_humidity, distance, wavelength
    ):
        """
        Calculate atmospheric absorption for different distances.
        :param ambient_temperature: List of ambient temperatures in degrees Celsius
        :param relative_humidity: List of relative humidity values (0 to 1)
        :param distance: List of distances in meters
        :param wavelength: Wavelength in micrometers
        :return: List of DataFrames with atmospheric absorption values
        """
        res_for_distance = []
        for dist in distance:
            table = pd.DataFrame(columns=relative_humidity)
            for tatm in ambient_temperature:
                temp_row = []
                for humidity in relative_humidity:
                    patm = self.atmospheric_transmission(
                        tatm, humidity, dist, wavelength
                    )
                    temp_row.append(patm)
                table.loc[tatm] = temp_row
            res_for_distance.append(table)
            print(f"distance: {dist}")
            print(table)
        return res_for_distance

    def absorption_per_wavelength(
        self, ambient_temperature, relative_humidity, distance, wavelength
    ):
        """
        Calculate atmospheric absorption for different wavelengths.
        :param ambient_temperature: List of ambient temperatures in degrees Celsius
        :param relative_humidity: List of relative humidity values (0 to 1)
        :param distance: Distance in meters
        :param wavelength: List of wavelengths in micrometers
        :return: List of DataFrames with atmospheric absorption values for each wavelength
        """
        res_for_wavelength = []
        for wave_l in wavelength:
            table = pd.DataFrame(columns=relative_humidity)
            for tatm in ambient_temperature:
                temp_row = []
                for humidity in relative_humidity:
                    patm = self.atmospheric_transmission(
                        tatm, humidity, distance, wave_l
                    )
                    temp_row.append(patm)
                table.loc[tatm] = temp_row
            res_for_wavelength.append(table)
            print(f"wavelength: {wave_l}")
            print(table)
        return res_for_wavelength


if __name__ == "__main__":
    # Compute atmospheric absorption
    vapout_table_filename = "passman larmore table for vapour absorbance.txt"
    carbon_dioxide_filename = (
        "passman larmore table for carbon dioxide absorbance.txt"
    )
    pl_model = PassmanLarmoreModel(
        vapout_table_filename, carbon_dioxide_filename
    )
    # Example from the paper:
    # patm = pl_model.atmospheric_transmission(
    #     tatm=20, humidity=0.5, distance=500, wavelength=13.0
    # )
    # print(patm)
    ambient_temperature = [0, 5, 10, 15, 20, 25, 30, 40, 45, 50]  # in degrees
    relative_humidity = [
        0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0
    ]  # in %
    distance = [0.5, 1, 1.5, 2, 2.5, 3, 4.5, 5, 500]  # in meters
    # Loaded wavelengths
    wavelength = [
        7.5, 8, 8.5, 9.0, 9.5, 10, 10.5, 11.0, 11.5, 12.0, 12.5,
        13.0, 13.5, 13.9
    ]
    # pl_model.absorption_per_distance(
    #     ambient_temperature, relative_humidity, distance, 13.0
    # )
    res = pl_model.absorption_per_wavelength(
        ambient_temperature, relative_humidity, 3, wavelength
    )
    print("Result of absorption_per_wavelength:")
    for i, df in enumerate(res):
        print(f"Wavelength: {wavelength[i]}")
        print(df)
        print()
    # -----------------------------------------------------------------------------------------------
    # Compute atmospheric scattering
    # atmospheric_scattering(8, 5)
