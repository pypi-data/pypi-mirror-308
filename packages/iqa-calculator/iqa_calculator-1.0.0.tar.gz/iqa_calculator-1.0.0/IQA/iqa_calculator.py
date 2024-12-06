import math

def WQI(oxigenio_dissolvido, coliformes_fecais, ph, dbo, nitrogenio_total, fosforo_total, turbidez, solidos_totais, altitude=None, temperatura=None) :
 return IQA(oxigenio_dissolvido, coliformes_fecais, ph, dbo, nitrogenio_total, fosforo_total, turbidez, solidos_totais, altitude, temperatura)

def IQA(
    oxigenio_dissolvido, coliformes_fecais, ph, dbo, nitrogenio_total, fosforo_total, turbidez, solidos_totais, altitude=None, temperatura=None
):
    """
    Function to calculate the Water Quality Index (IQA).

    Parameters:
        oxigenio_dissolvido (float): Dissolved Oxygen.
        coliformes_fecais (float): Fecal Coliforms.
        ph (float): pH value.
        dbo (float): Biochemical Oxygen Demand (BOD).
        nitrogenio_total (float): Total Nitrogen.
        fosforo_total (float): Total Phosphorus (mg/L or converted as per option).
        turbidez (float): Turbidity.
        solidos_totais (float): Total Solids.
        altitude (float, optional): Altitude (in meters). Defaults to 200 if not provided.
        temperatura (float, optional): Temperature (in ºC). Defaults to 22 if not provided.

    Returns:
        dict: A dictionary containing the IQA value and the water quality classification.
    """

    # Set default values for altitude and temperature if not provided
    if altitude is None:
        altitude = 200
    if temperatura is None:
        temperatura = 22

    # Dissolved Oxygen
    # Calculate saturation concentration based on temperature and altitude
    concentracao_saturacao = (
        (14.62 - 0.3898 * temperatura + 0.006969 * temperatura**2 - 0.00005896 * temperatura**3)
        * (1 - 0.0000228675 * altitude) ** 5.167
    )
    perc_saturacao = 100 * oxigenio_dissolvido / concentracao_saturacao

    # Calculate Dissolved Oxygen weight based on saturation percentage
    if perc_saturacao > 0 and perc_saturacao <= 50:
        resultado_od = 3 + 0.34 * perc_saturacao + 0.008095 * perc_saturacao**2 + 1.35252 * 0.00001 * perc_saturacao**3
    elif perc_saturacao > 50 and perc_saturacao <= 85:
        resultado_od = 3 - 1.166 * perc_saturacao + 0.058 * perc_saturacao - 3.803435 * 0.00001 * perc_saturacao**3
    elif perc_saturacao > 85 and perc_saturacao <= 100:
        resultado_od = 3 + 3.7745 * perc_saturacao**0.704889
    elif perc_saturacao > 100 and perc_saturacao <= 140:
        resultado_od = 3 + 2.9 * perc_saturacao - 0.02496 * perc_saturacao**2 + 5.60919 * 0.00001 * perc_saturacao**3
    else:
        resultado_od = 3 + 47
    peso_od = resultado_od**0.17  # Apply weight to the Dissolved Oxygen result

    # Fecal Coliforms
    # Convert to log10 and calculate weight based on conditions
    coliformes_fecais = math.log10(coliformes_fecais)
    if coliformes_fecais > 0 and coliformes_fecais <= 1:
        resultado_cf = 100 - 33 * coliformes_fecais
    elif coliformes_fecais > 1 and coliformes_fecais <= 5:
        resultado_cf = 100 - 37.2 * coliformes_fecais + 3.60743 * coliformes_fecais**2
    else:
        resultado_cf = 3
    peso_cf = resultado_cf**0.15

    # pH
    # Calculate weight based on pH intervals
    if ph > 0 and ph <= 2:
        resultado_ph = 2.0
    elif ph > 2 and ph <= 4:
        resultado_ph = 13.6 - 10.6 * ph + 2.4364 * ph**2
    elif ph > 4 and ph <= 6.2:
        resultado_ph = 155.5 - 77.36 * ph + 10.2481 * ph**2
    elif ph > 6.2 and ph <= 7:
        resultado_ph = -657.2 + 197.38 * ph - 12.9167 * ph**2
    elif ph > 7 and ph <= 8:
        resultado_ph = -427.8 + 142.05 * ph - 9.695 * ph**2
    elif ph > 8 and ph <= 8.5:
        resultado_ph = 216 - 16 * ph
    elif ph > 8.5 and ph <= 9:
        resultado_ph = 1415823 * math.exp(-1.1507 * ph)
    elif ph > 9 and ph <= 10:
        resultado_ph = 228 - 27 * ph
    elif ph > 10 and ph <= 12:
        resultado_ph = 633 - 106.5 * ph + 4.5 * ph**2
    else:
        resultado_ph = 3.0
    peso_ph = resultado_ph**0.12

    # Biochemical Oxygen Demand (BOD)
    # Calculate weight based on BOD value
    if dbo > 0 and dbo <= 5:
        resultado_dbo = 99.96 * math.exp(-0.1232728 * dbo)
    elif dbo > 5 and dbo <= 15:
        resultado_dbo = 104.67 - 31.5463 * math.log10(dbo)
    elif dbo > 15 and dbo <= 30:
        resultado_dbo = 4394.91 * dbo**-1.99809
    else:
        resultado_dbo = 2
    peso_dbo = resultado_dbo**0.10

    # Total Nitrogen
    # Calculate weight based on Total Nitrogen
    if nitrogenio_total > 0 and nitrogenio_total <= 10:
        resultado_nt = 100 - 8.169 * nitrogenio_total + 0.3059 * nitrogenio_total**2
    elif nitrogenio_total > 10 and nitrogenio_total <= 60:
        resultado_nt = 101.9 - 23.1023 * math.log10(nitrogenio_total)
    elif nitrogenio_total > 60 and nitrogenio_total <= 100:
        resultado_nt = 159.3148 * math.exp(-0.0512842 * nitrogenio_total)
    else:
        resultado_nt = 1
    peso_nt = resultado_nt**0.10

    # Total Phosphorus
    # Calculate weight based on Total Phosphorus value
    if fosforo_total > 0 and fosforo_total <= 1:
        resultado_ft = 99 * math.exp(-0.91629 * fosforo_total)
    elif fosforo_total > 1 and fosforo_total <= 5:
        resultado_ft = 57.6 - 20.178 * fosforo_total + 2.1326 * fosforo_total**2
    elif fosforo_total > 5 and fosforo_total <= 10:
        resultado_ft = 19.8 * math.exp(-0.13544 * fosforo_total)
    else:
        resultado_ft = 5.0
    peso_ft = resultado_ft**0.10

    # Turbidity
    # Calculate weight based on Turbidity value
    if turbidez > 0 and turbidez <= 25:
        resultado_tb = 100.17 - 2.67 * turbidez + 0.03775 * turbidez**2
    elif turbidez > 25 and turbidez <= 100:
        resultado_tb = 84.76 * math.exp(-0.016206 * turbidez)
    else:
        resultado_tb = 5
    peso_tb = resultado_tb**0.08

    # Total Solids
    # Calculate weight based on Total Solids value
    if solidos_totais > 0 and solidos_totais <= 150:
        resultado_st = 79.75 + 0.166 * solidos_totais - 0.001088 * solidos_totais**2
    elif solidos_totais > 150 and solidos_totais <= 500:
        resultado_st = 101.67 - 0.13917 * solidos_totais
    else:
        resultado_st = 32
    peso_st = resultado_st**0.08

    # Temperature weight constant
    peso_temp = 94.0**0.10

    # Final IQA calculation
    iqa = peso_od * peso_cf * peso_ph * peso_dbo * peso_nt * peso_ft * peso_temp * peso_tb * peso_st

    # Determine water quality classification
    if iqa <= 19:
        qualidade = "Péssima"  # "Very Bad"
    elif iqa > 19 and iqa <= 36:
        qualidade = "Ruim"  # "Poor"
    elif iqa > 36 and iqa <= 51:
        qualidade = "Regular"  # "Fair"
    elif iqa > 51 and iqa <= 79:
        qualidade = "Boa"  # "Good"
    else:
        qualidade = "Ótima"  # "Excellent"

    return {"iqa": round(iqa, 2), "qualidade": qualidade}
