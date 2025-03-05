/**
 * NOTE: Input automata, that are of type `NFA-bits` are mintermized!
 *  - If you want to skip mintermization, set the variable `MINTERMIZE_AUTOMATA` below to `false`
 */

#include "utils/utils.hh"
#include "mata/nfa/nfa.hh"

#include <iostream>
#include <iomanip>
#include <mata/nfa/types.hh>
#include <ostream>
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

    // Evaluate time
    if (algorithm == "simulation"){
        TIME_BEGIN(reduction);
    
        result = mata::nfa::reduce(aut, 0, ParameterMap{{"algorithm", algorithm}, {"direction", "forward"}});

        TIME_END(reduction);
    }
    else if (algorithm == "residual"){
        TIME_BEGIN(reduction);

        result = mata::nfa::reduce(aut, 0, ParameterMap{{"algorithm", algorithm}, {"type", "with"}, {"direction", "forward"}});

        TIME_END(reduction);
    }
    else if (algorithm == "brzozowski"){
        TIME_BEGIN(reduction);

        result = mata::nfa::minimize(aut, ParameterMap{{"algorithm", algorithm}});

        TIME_END(reduction);
    }
    else if (algorithm == "hopcroft"){
        TIME_BEGIN(reduction);

        result = mata::nfa::minimize(aut, ParameterMap{{"algorithm", algorithm}});

        TIME_END(reduction);
    }
    else{
        return EXIT_FAILURE;
    }

    // Evaluate the number of states and transitions
    std::cout << "states: " << result.num_of_states() << std::endl;
    std::cout << "transitions: " << result.delta.num_of_transitions() << std::endl;


    return EXIT_SUCCESS;
}
