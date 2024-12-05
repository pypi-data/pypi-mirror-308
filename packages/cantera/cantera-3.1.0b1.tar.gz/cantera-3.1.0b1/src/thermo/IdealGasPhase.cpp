/**
 *  @file IdealGasPhase.cpp
 *   ThermoPhase object for the ideal gas equation of
 * state - workhorse for %Cantera (see @ref thermoprops
 * and class @link Cantera::IdealGasPhase IdealGasPhase@endlink).
 */

// This file is part of Cantera. See License.txt in the top-level directory or
// at https://cantera.org/license.txt for license and copyright information.

#include "cantera/thermo/IdealGasPhase.h"
#include "cantera/thermo/ThermoFactory.h"
#include "cantera/base/utilities.h"

namespace Cantera
{

IdealGasPhase::IdealGasPhase(const string& inputFile, const string& id_)
{
    initThermoFile(inputFile, id_);
}

// Molar Thermodynamic Properties of the Solution ------------------

double IdealGasPhase::entropy_mole() const
{
    return GasConstant * (mean_X(entropy_R_ref()) - sum_xlogx() - std::log(pressure() / refPressure()));
}

double IdealGasPhase::cp_mole() const
{
    return GasConstant * mean_X(cp_R_ref());
}

double IdealGasPhase::cv_mole() const
{
    return cp_mole() - GasConstant;
}

double IdealGasPhase::soundSpeed() const {
    return sqrt(
        cp_mole() / cv_mole() * GasConstant / meanMolecularWeight() * temperature()
    );
}

double IdealGasPhase::standardConcentration(size_t k) const
{
    return pressure() / RT();
}

void IdealGasPhase::getActivityCoefficients(double* ac) const
{
    for (size_t k = 0; k < m_kk; k++) {
        ac[k] = 1.0;
    }
}

void IdealGasPhase::getStandardChemPotentials(double* muStar) const
{
    getGibbs_ref(muStar);
    double tmp = log(pressure() / refPressure()) * RT();
    for (size_t k = 0; k < m_kk; k++) {
        muStar[k] += tmp; // add RT*ln(P/P_0)
    }
}

//  Partial Molar Properties of the Solution --------------

void IdealGasPhase::getChemPotentials(double* mu) const
{
    getStandardChemPotentials(mu);
    for (size_t k = 0; k < m_kk; k++) {
        double xx = std::max(SmallNumber, moleFraction(k));
        mu[k] += RT() * log(xx);
    }
}

void IdealGasPhase::getPartialMolarEnthalpies(double* hbar) const
{
    const vector<double>& _h = enthalpy_RT_ref();
    scale(_h.begin(), _h.end(), hbar, RT());
}

void IdealGasPhase::getPartialMolarEntropies(double* sbar) const
{
    const vector<double>& _s = entropy_R_ref();
    scale(_s.begin(), _s.end(), sbar, GasConstant);
    double logp = log(pressure() / refPressure());
    for (size_t k = 0; k < m_kk; k++) {
        double xx = std::max(SmallNumber, moleFraction(k));
        sbar[k] += GasConstant * (-logp - log(xx));
    }
}

void IdealGasPhase::getPartialMolarIntEnergies(double* ubar) const
{
    const vector<double>& _h = enthalpy_RT_ref();
    for (size_t k = 0; k < m_kk; k++) {
        ubar[k] = RT() * (_h[k] - 1.0);
    }
}

void IdealGasPhase::getPartialMolarCp(double* cpbar) const
{
    const vector<double>& _cp = cp_R_ref();
    scale(_cp.begin(), _cp.end(), cpbar, GasConstant);
}

void IdealGasPhase::getPartialMolarVolumes(double* vbar) const
{
    double vol = 1.0 / molarDensity();
    for (size_t k = 0; k < m_kk; k++) {
        vbar[k] = vol;
    }
}

// Properties of the Standard State of the Species in the Solution --

void IdealGasPhase::getEnthalpy_RT(double* hrt) const
{
    const vector<double>& _h = enthalpy_RT_ref();
    copy(_h.begin(), _h.end(), hrt);
}

void IdealGasPhase::getEntropy_R(double* sr) const
{
    const vector<double>& _s = entropy_R_ref();
    copy(_s.begin(), _s.end(), sr);
    double tmp = log(pressure() / refPressure());
    for (size_t k = 0; k < m_kk; k++) {
        sr[k] -= tmp;
    }
}

void IdealGasPhase::getGibbs_RT(double* grt) const
{
    const vector<double>& gibbsrt = gibbs_RT_ref();
    copy(gibbsrt.begin(), gibbsrt.end(), grt);
    double tmp = log(pressure() / refPressure());
    for (size_t k = 0; k < m_kk; k++) {
        grt[k] += tmp;
    }
}

void IdealGasPhase::getPureGibbs(double* gpure) const
{
    const vector<double>& gibbsrt = gibbs_RT_ref();
    scale(gibbsrt.begin(), gibbsrt.end(), gpure, RT());
    double tmp = log(pressure() / refPressure()) * RT();
    for (size_t k = 0; k < m_kk; k++) {
        gpure[k] += tmp;
    }
}

void IdealGasPhase::getIntEnergy_RT(double* urt) const
{
    getIntEnergy_RT_ref(urt);
}

void IdealGasPhase::getCp_R(double* cpr) const
{
    const vector<double>& _cpr = cp_R_ref();
    copy(_cpr.begin(), _cpr.end(), cpr);
}

void IdealGasPhase::getStandardVolumes(double* vol) const
{
    double tmp = 1.0 / molarDensity();
    for (size_t k = 0; k < m_kk; k++) {
        vol[k] = tmp;
    }
}

// Thermodynamic Values for the Species Reference States ---------

void IdealGasPhase::getEnthalpy_RT_ref(double* hrt) const
{
    const vector<double>& _h = enthalpy_RT_ref();
    copy(_h.begin(), _h.end(), hrt);
}

void IdealGasPhase::getGibbs_RT_ref(double* grt) const
{
    const vector<double>& gibbsrt = gibbs_RT_ref();
    copy(gibbsrt.begin(), gibbsrt.end(), grt);
}

void IdealGasPhase::getGibbs_ref(double* g) const
{
    const vector<double>& gibbsrt = gibbs_RT_ref();
    scale(gibbsrt.begin(), gibbsrt.end(), g, RT());
}

void IdealGasPhase::getEntropy_R_ref(double* er) const
{
    const vector<double>& _s = entropy_R_ref();
    copy(_s.begin(), _s.end(), er);
}

void IdealGasPhase::getIntEnergy_RT_ref(double* urt) const
{
    const vector<double>& _h = enthalpy_RT_ref();
    for (size_t k = 0; k < m_kk; k++) {
        urt[k] = _h[k] - 1.0;
    }
}

void IdealGasPhase::getCp_R_ref(double* cprt) const
{
    const vector<double>& _cpr = cp_R_ref();
    copy(_cpr.begin(), _cpr.end(), cprt);
}

void IdealGasPhase::getStandardVolumes_ref(double* vol) const
{
    double tmp = RT() / m_p0;
    for (size_t k = 0; k < m_kk; k++) {
        vol[k] = tmp;
    }
}

bool IdealGasPhase::addSpecies(shared_ptr<Species> spec)
{
    bool added = ThermoPhase::addSpecies(spec);
    if (added) {
        if (m_kk == 1) {
            m_p0 = refPressure();
        }
        m_h0_RT.push_back(0.0);
        m_g0_RT.push_back(0.0);
        m_expg0_RT.push_back(0.0);
        m_cp0_R.push_back(0.0);
        m_s0_R.push_back(0.0);
        m_pp.push_back(0.0);
    }
    return added;
}

void IdealGasPhase::setToEquilState(const double* mu_RT)
{
    const vector<double>& grt = gibbs_RT_ref();

    // Within the method, we protect against inf results if the exponent is too
    // high.
    //
    // If it is too low, we set the partial pressure to zero. This capability is
    // needed by the elemental potential method.
    double pres = 0.0;
    for (size_t k = 0; k < m_kk; k++) {
        double tmp = -grt[k] + mu_RT[k];
        if (tmp < -600.) {
            m_pp[k] = 0.0;
        } else if (tmp > 300.0) {
            double tmp2 = tmp / 300.;
            tmp2 *= tmp2;
            m_pp[k] = m_p0 * exp(300.) * tmp2;
        } else {
            m_pp[k] = m_p0 * exp(tmp);
        }
        pres += m_pp[k];
    }
    // set state
    setMoleFractions(m_pp.data());
    setPressure(pres);
}

void IdealGasPhase::updateThermo() const
{
    static const int cacheId = m_cache.getId();
    CachedScalar cached = m_cache.getScalar(cacheId);
    double tnow = temperature();

    // If the temperature has changed since the last time these
    // properties were computed, recompute them.
    if (cached.state1 != tnow) {
        m_spthermo.update(tnow, &m_cp0_R[0], &m_h0_RT[0], &m_s0_R[0]);
        cached.state1 = tnow;

        // update the species Gibbs functions
        for (size_t k = 0; k < m_kk; k++) {
            m_g0_RT[k] = m_h0_RT[k] - m_s0_R[k];
        }
    }
}
}
