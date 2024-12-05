/**
 *  @file stringUtils.cpp
 * Contains definitions for string manipulation functions
 *       within Cantera.
 */

// This file is part of Cantera. See License.txt in the top-level directory or
// at https://cantera.org/license.txt for license and copyright information.

//@{
#include "cantera/base/ct_defs.h"

#ifdef _MSC_VER
#define SNPRINTF _snprintf
#else
#define SNPRINTF snprintf
#endif
//@}

#include "cantera/base/stringUtils.h"
#include "cantera/base/ctexceptions.h"
#include "cantera/base/utilities.h"
#include "cantera/base/global.h"

#include <boost/algorithm/string.hpp>
#include <sstream>

namespace ba = boost::algorithm;

namespace Cantera
{

string vec2str(const vector<double>& v, const string& fmt, const string& sep)
{
    char buf[64];
    std::stringstream o;
    for (size_t i = 0; i < v.size(); i++) {
        SNPRINTF(buf, 63, fmt.c_str(), v[i]);
        o << buf;
        if (i != v.size() - 1) {
            o << sep;
        }
    }
    return o.str();
}

string stripnonprint(const string& s)
{
    string ss = "";
    for (size_t i = 0; i < s.size(); i++) {
        if (isprint(s[i])) {
            ss += s[i];
        }
    }
    return ss;
}

Composition parseCompString(const string& ss, const vector<string>& names)
{
    Composition x;
    for (size_t k = 0; k < names.size(); k++) {
        x[names[k]] = 0.0;
    }

    size_t start = 0;
    size_t stop = 0;
    size_t left = 0;
    while (stop < ss.size()) {
        size_t colon = ss.find(':', left);
        if (colon == npos) {
            break;
        }
        size_t valstart = ss.find_first_not_of(" \t\n", colon+1);
        stop = ss.find_first_of(", ;\n\t", valstart);
        string name = ba::trim_copy(ss.substr(start, colon-start));
        if (!names.empty() && x.find(name) == x.end()) {
            throw CanteraError("parseCompString",
                "unknown species '" + name + "'");
        }

        double value;
        try {
            value = fpValueCheck(ss.substr(valstart, stop-valstart));
        } catch (CanteraError&) {
            // If we have a key containing a colon, we expect this to fail. In
            // this case, take the current substring as part of the key and look
            // to the right of the next colon for the corresponding value.
            // Otherwise, this is an invalid composition string.
            string testname = ss.substr(start, stop-start);
            if (testname.find_first_of(" \n\t") != npos) {
                // Space, tab, and newline are never allowed in names
                throw;
            } else if (ss.substr(valstart, stop-valstart).find(':') != npos) {
                left = colon + 1;
                stop = 0; // Force another iteration of this loop
                continue;
            } else {
                throw;
            }
        }
        if (getValue(x, name, 0.0) != 0.0) {
            throw CanteraError("parseCompString",
                               "Duplicate key: '" + name + "'.");
        }

        x[name] = value;
        start = ss.find_first_not_of(", ;\n\t", stop+1);
        left = start;
    }
    if (left != start) {
        throw CanteraError("parseCompString", "Unable to parse key-value pair:"
            "\n'{}'", ss.substr(start, stop));
    }
    if (stop != npos && !ba::trim_copy(ss.substr(stop)).empty()) {
        throw CanteraError("parseCompString", "Found non-key:value data "
            "in composition string: '" + ss.substr(stop) + "'");
    }
    return x;
}

double fpValue(const string& val)
{
    double rval;
    std::stringstream ss(val);
    ss.imbue(std::locale("C"));
    ss >> rval;
    return rval;
}

double fpValueCheck(const string& val)
{
    string str = ba::trim_copy(val);
    if (str.empty()) {
        throw CanteraError("fpValueCheck", "string has zero length");
    }
    int numDot = 0;
    int numExp = 0;
    char ch;
    int istart = 0;
    ch = str[0];
    if (ch == '+' || ch == '-') {
        if (str.size() == 1) {
            throw CanteraError("fpValueCheck", "string '{}' ends in '{}'", val, ch);
        }
        istart = 1;
    }
    for (size_t i = istart; i < str.size(); i++) {
        ch = str[i];
        if (isdigit(ch)) {
        } else if (ch == '.') {
            numDot++;
            if (numDot > 1) {
                throw CanteraError("fpValueCheck",
                                   "string '{}' has more than one decimal point.", val);
            }
            if (numExp > 0) {
                throw CanteraError("fpValueCheck",
                                   "string '{}' has decimal point in exponent", val);
            }
        } else if (ch == 'e' || ch == 'E' || ch == 'd' || ch == 'D') {
            numExp++;
            str[i] = 'E';
            if (numExp > 1) {
                throw CanteraError("fpValueCheck",
                                   "string '{}' has more than one exp char", val);
            } else if (i == str.size() - 1) {
                throw CanteraError("fpValueCheck", "string '{}' ends in '{}'", val, ch);
            }
            ch = str[i+1];
            if (ch == '+' || ch == '-') {
                if (i + 1 == str.size() - 1) {
                    throw CanteraError("fpValueCheck",
                                       "string '{}' ends in '{}'", val, ch);
                }
                i++;
            }
        } else {
            throw CanteraError("fpValueCheck", "Trouble processing string '{}'", str);
        }
    }
    return fpValue(str);
}

void tokenizeString(const string& in_val, vector<string>& v)
{
    string val = ba::trim_copy(in_val);
    v.clear();
    if (val.empty()) {
        // In this case, prefer v to be empty instead of split's behavior of
        // returning a vector with one element that is the empty string.
        return;
    }
    ba::split(v, val, ba::is_space(), ba::token_compress_on);
}

void tokenizePath(const string& in_val, vector<string>& v)
{
    string val = ba::trim_copy(in_val);
    v.clear();
    ba::split(v, val, ba::is_any_of("/\\"), ba::token_compress_on);
}

size_t copyString(const string& source, char* dest, size_t length)
{
    const char* c_src = source.c_str();
    size_t N = std::min(length, source.length()+1);
    size_t ret = (length >= source.length() + 1) ? 0 : source.length() + 1;
    std::copy(c_src, c_src + N, dest);
    if (length != 0) {
        dest[length-1] = '\0';
    }
    return ret;
}

string trimCopy(const string &input) {
    return ba::trim_copy(input);
}

string toLowerCopy(const string &input) {
    return ba::to_lower_copy(input);
}

bool caseInsensitiveEquals(const string &input, const string &test) {
    return ba::iequals(input, test);
}

}
