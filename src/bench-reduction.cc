/**
 * NOTE: Input automata, that are of type `NFA-bits` are mintermized!
 *  - If you want to skip mintermization, set the variable `MINTERMIZE_AUTOMATA` below to `false`
 */

#include "mata/nfa/algorithms.hh"
#include "utils/utils.hh"
#include "mata/nfa/nfa.hh"

#include <iostream>
#include <iomanip>
#include <mata/nfa/types.hh>
#include <string>

using namespace mata::nfa;

const bool MINTERMIZE_AUTOMATA = false;

int main(int argc, char *argv[])
{
    if (argc != 3) {
        std::cerr << "Something is missing\n";
        return EXIT_FAILURE;
    }

    std::string filename = argv[1];
    std::string algorithm = argv[2];

    Nfa aut;
    Nfa result;
    mata::OnTheFlyAlphabet alphabet{};
    if (load_automaton(filename, aut, alphabet, MINTERMIZE_AUTOMATA) != EXIT_SUCCESS) {
        return EXIT_FAILURE;
    }

    // Setting precision of the times to fixed points and 4 decimal places
    std::cout << std::fixed << std::setprecision(4);

    if (algorithm == "simulation"){
        TIME_BEGIN(relation);
    
        result = mata::nfa::reduce(aut, 0, ParameterMap{{"algorithm", algorithm}});

        TIME_END(relation);

    }
    else if (algorithm == "residual"){
        TIME_BEGIN(relation);

        result = mata::nfa::reduce(aut, 0, ParameterMap{{"algorithm", algorithm}, {"type", "with"}, {"direction", "forward"}});

        TIME_END(relation);
    }
    else if (algorithm == "brzozowski"){
        TIME_BEGIN(relation);

        result = mata::nfa::minimize(aut, ParameterMap{{"algorithm", algorithm}});

        TIME_END(relation);
    }
    else if (algorithm == "hopkroft"){
        TIME_BEGIN(relation);

        result = mata::nfa::minimize(aut, ParameterMap{{"algorithm", algorithm}});

        TIME_END(relation);
    }
    else{
        return EXIT_FAILURE;
    }

    return EXIT_SUCCESS;
}
