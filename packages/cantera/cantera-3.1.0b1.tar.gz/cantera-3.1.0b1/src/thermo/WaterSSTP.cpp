/**
 *  @file WaterSSTP.cpp
 * Definitions for a ThermoPhase class consisting of pure water (see @ref thermoprops
 * and class @link Cantera::WaterSSTP WaterSSTP@endlink).
 */

// This file is part of Cantera. See License.txt in the top-level directory or
// at https://cantera.org/license.txt for license and copyright information.

#include "cantera/thermo/WaterSSTP.h"
#include "cantera/thermo/ThermoFactory.h"
#include "cantera/base/stringUtils.h"

namespace Cantera
{
WaterSSTP::WaterSSTP(const string& inputFile, const string& id)
{
    initThermoFile(inputFile, id);
}

string WaterSSTP::phaseOfMatter() const {
    const vector<string> phases = {
        "gas", "liquid", "supercritical", "unstable-liquid", "unstable-gas"
    };
    return phases[m_sub.phaseState()];
}

void WaterSSTP::initThermo()
{
    SingleSpeciesTP::initThermo();

    // Calculate the molecular weight. Note while there may be a very good
    // calculated weight in the steam table class, using this weight may lead to
    // codes exhibiting mass loss issues. We need to grab the elemental atomic
    // weights used in the Element class and calculate a consistent H2O
    // molecular weight based on that.
    size_t nH = elementIndex("H");
    if (nH == npos) {
        throw CanteraError("WaterSSTP::initThermo",
                           "H not an element");
    }
    double mw_H = atomicWeight(nH);
    size_t nO = elementIndex("O");
    if (nO == npos) {
        throw CanteraError("WaterSSTP::initThermo",
                           "O not an element");
    }
    double mw_O = atomicWeight(nO);
    m_mw = 2.0 * mw_H + mw_O;
    setMolecularWeight(0,m_mw);

    // Set the baseline
    double T = 298.15;
    Phase::setDensity(7.0E-8);
    Phase::setTemperature(T);

    double presLow = 1.0E-2;
    double oneBar = 1.0E5;
    double dd = m_sub.density(T, presLow, WATER_GAS, 7.0E-8);
    setDensity(dd);
    setTemperature(T);
    SW_Offset = 0.0;
    double s = entropy_mole();
    s -= GasConstant * log(oneBar/presLow);
    if (s != 188.835E3) {
        SW_Offset = 188.835E3 - s;
    }
    s = entropy_mole();
    s -= GasConstant * log(oneBar/presLow);

    double h = enthalpy_mole();
    if (h != -241.826E6) {
        EW_Offset = -241.826E6 - h;
    }
    h = enthalpy_mole();

    // Set the initial state of the system to 298.15 K and 1 bar.
    setTemperature(298.15);
    double rho0 = m_sub.density(298.15, OneAtm, WATER_LIQUID);
    setDensity(rho0);

    m_waterProps = make_unique<WaterProps>(&m_sub);

    // Set the flag to say we are ready to calculate stuff
    m_ready = true;
}

void WaterSSTP::getEnthalpy_RT(double* hrt) const
{
    *hrt = (m_sub.enthalpy_mass() * m_mw + EW_Offset) / RT();
}

void WaterSSTP::getIntEnergy_RT(double* ubar) const
{
    *ubar = (m_sub.intEnergy_mass() * m_mw + EW_Offset)/ RT();
}

void WaterSSTP::getEntropy_R(double* sr) const
{
    sr[0] = (m_sub.entropy_mass() * m_mw + SW_Offset) / GasConstant;
}

void WaterSSTP::getGibbs_RT(double* grt) const
{
    *grt = (m_sub.gibbs_mass() * m_mw + EW_Offset) / RT()
           - SW_Offset / GasConstant;
    if (!m_ready) {
        throw CanteraError("waterSSTP::getGibbs_RT", "Phase not ready");
    }
}

void WaterSSTP::getStandardChemPotentials(double* gss) const
{
    *gss = (m_sub.gibbs_mass() * m_mw + EW_Offset - SW_Offset*temperature());
    if (!m_ready) {
        throw CanteraError("waterSSTP::getStandardChemPotentials",
                           "Phase not ready");
    }
}

void WaterSSTP::getCp_R(double* cpr) const
{
    cpr[0] = m_sub.cp_mass() * m_mw / GasConstant;
}

double WaterSSTP::cv_mole() const
{
    return m_sub.cv_mass() * m_mw;
}

void WaterSSTP::getEnthalpy_RT_ref(double* hrt) const
{
    double p = pressure();
    double T = temperature();
    double dens = density();
    int waterState = WATER_GAS;
    double rc = m_sub.Rhocrit();
    if (dens > rc) {
        waterState = WATER_LIQUID;
    }
    double dd = m_sub.density(T, OneAtm, waterState, dens);
    if (dd <= 0.0) {
        throw CanteraError("WaterSSTP::getEnthalpy_RT_ref", "error");
    }
    double h = m_sub.enthalpy_mass() * m_mw;
    *hrt = (h + EW_Offset) / RT();
    dd = m_sub.density(T, p, waterState, dens);
}

void WaterSSTP::getGibbs_RT_ref(double* grt) const
{
    double p = pressure();
    double T = temperature();
    double dens = density();
    int waterState = WATER_GAS;
    double rc = m_sub.Rhocrit();
    if (dens > rc) {
        waterState = WATER_LIQUID;
    }
    double dd = m_sub.density(T, OneAtm, waterState, dens);
    if (dd <= 0.0) {
        throw CanteraError("WaterSSTP::getGibbs_RT_ref", "error");
    }
    m_sub.setState_TD(T, dd);
    double g = m_sub.gibbs_mass() * m_mw;
    *grt = (g + EW_Offset - SW_Offset*T)/ RT();
    dd = m_sub.density(T, p, waterState, dens);
}

void WaterSSTP::getGibbs_ref(double* g) const
{
    getGibbs_RT_ref(g);
    for (size_t k = 0; k < m_kk; k++) {
        g[k] *= RT();
    }
}

void WaterSSTP::getEntropy_R_ref(double* sr) const
{
    double p = pressure();
    double T = temperature();
    double dens = density();
    int waterState = WATER_GAS;
    double rc = m_sub.Rhocrit();
    if (dens > rc) {
        waterState = WATER_LIQUID;
    }
    double dd = m_sub.density(T, OneAtm, waterState, dens);

    if (dd <= 0.0) {
        throw CanteraError("WaterSSTP::getEntropy_R_ref", "error");
    }
    m_sub.setState_TD(T, dd);

    double s = m_sub.entropy_mass() * m_mw;
    *sr = (s + SW_Offset)/ GasConstant;
    dd = m_sub.density(T, p, waterState, dens);
}

void WaterSSTP::getCp_R_ref(double* cpr) const
{
    double p = pressure();
    double T = temperature();
    double dens = density();
    int waterState = WATER_GAS;
    double rc = m_sub.Rhocrit();
    if (dens > rc) {
        waterState = WATER_LIQUID;
    }
    double dd = m_sub.density(T, OneAtm, waterState, dens);
    m_sub.setState_TD(T, dd);
    if (dd <= 0.0) {
        throw CanteraError("WaterSSTP::getCp_R_ref", "error");
    }
    double cp = m_sub.cp_mass() * m_mw;
    *cpr = cp / GasConstant;
    dd = m_sub.density(T, p, waterState, dens);
}

void WaterSSTP::getStandardVolumes_ref(double* vol) const
{
    double p = pressure();
    double T = temperature();
    double dens = density();
    int waterState = WATER_GAS;
    double rc = m_sub.Rhocrit();
    if (dens > rc) {
        waterState = WATER_LIQUID;
    }
    double dd = m_sub.density(T, OneAtm, waterState, dens);
    if (dd <= 0.0) {
        throw CanteraError("WaterSSTP::getStandardVolumes_ref", "error");
    }
    *vol = meanMolecularWeight() /dd;
    dd = m_sub.density(T, p, waterState, dens);
}

double WaterSSTP::pressure() const
{
    return m_sub.pressure();
}

void WaterSSTP::setPressure(double p)
{
    double T = temperature();
    double dens = density();
    double pp = m_sub.psat(T);
    int waterState = WATER_SUPERCRIT;
    if (T < m_sub.Tcrit()) {
        if (p >= pp) {
            waterState = WATER_LIQUID;
            dens = 1000.;
        } else if (!m_allowGasPhase) {
            throw CanteraError("WaterSSTP::setPressure",
                "Model assumes liquid phase; pressure p = {} lies below\n"
                "the saturation pressure (P_sat = {}).", p, pp);
        }
    }

    double dd = m_sub.density(T, p, waterState, dens);
    if (dd <= 0.0) {
        throw CanteraError("WaterSSTP::setPressure", "Error");
    }
    setDensity(dd);
}

double WaterSSTP::isothermalCompressibility() const
{
    return m_sub.isothermalCompressibility();
}

double WaterSSTP::thermalExpansionCoeff() const
{
    return m_sub.coeffThermExp();
}

double WaterSSTP::dthermalExpansionCoeffdT() const
{
    double pres = pressure();
    double dens_save = density();
    double T = temperature();
    double tt = T - 0.04;
    double dd = m_sub.density(tt, pres, WATER_LIQUID, dens_save);
    if (dd < 0.0) {
        throw CanteraError("WaterSSTP::dthermalExpansionCoeffdT",
            "Unable to solve for the density at T = {}, P = {}", tt, pres);
    }
    double vald = m_sub.coeffThermExp();
    m_sub.setState_TD(T, dens_save);
    double val2 = m_sub.coeffThermExp();
    return (val2 - vald) / 0.04;
}

double WaterSSTP::critTemperature() const
{
    return m_sub.Tcrit();
}

double WaterSSTP::critPressure() const
{
    return m_sub.Pcrit();
}

double WaterSSTP::critDensity() const
{
    return m_sub.Rhocrit();
}

void WaterSSTP::setTemperature(const double temp)
{
    if (temp < 273.16) {
        throw CanteraError("WaterSSTP::setTemperature",
            "Model assumes liquid phase; temperature T = {} lies below\n"
            "the triple point temperature (T_triple = 273.16).", temp);
    }
    Phase::setTemperature(temp);
    m_sub.setState_TD(temp, density());
}

void WaterSSTP::setDensity(const double dens)
{
    Phase::setDensity(dens);
    m_sub.setState_TD(temperature(), dens);
}

double WaterSSTP::satPressure(double t) {
    double tsave = temperature();
    double dsave = density();
    double pp = m_sub.psat(t);
    m_sub.setState_TD(tsave, dsave);
    return pp;
}

double WaterSSTP::vaporFraction() const
{
    if (temperature() >= m_sub.Tcrit()) {
        double dens = density();
        if (dens >= m_sub.Rhocrit()) {
            return 0.0;
        }
        return 1.0;
    }
    // If below tcrit we always return 0 from this class
    return 0.0;
}

}
