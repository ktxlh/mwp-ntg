from collections import Counter

####
# for other_mwp statistics only
total_data_len = 1557
####

# TODO: > .md in gen, how about segs??

def _print_md_col_names(items):
    ## Print the first 2 lines of a .MarkDown table
    print(f"| {' | '.join([str(item) for item in items])} |")
    print(f"| {' | '.join(['-'*8 for item in items])} |")

def top_templates_from_train(top_temps, temps2sents, metadata, metadata_colnames=None, k=5, n=3): 
    """
    Parameters:
    ----------
        k:   int
            Max number of top templates to print
        n:   int
            Max number of sentence samples to print for each template
    """   

    if k > len(top_temps):
        print(f"Warning: k={k} > len(top_temps) => k := {len(top_temps)}")
        k = len(top_temps)
    
    # HACK If too many catogeries (e.g. 'questions'), don't print it
    some_cnames = [cname for cname in metadata_colnames if len(set(metadata[cname])) < 15]
    
    for i in range(k):  # Print top k tamplates
        sents = temps2sents[top_temps[i]]
        
        N = len(sents)
        print(f"### Top-{i+1} ({N}): {top_temps[i]}")

        if metadata_colnames == None:
            metadata_colnames=list(metadata)
        _print_md_col_names([*(top_temps[i]), *metadata_colnames])#, 'lineno', 'count', 'portion'])

        duplicated = Counter()     # Counter for duplicated templates
        j = 0
        for sent in sents:
            if j == n:      # HACK Print only n samples
                break
            lineno = sent[1]
            attrs = [str(metadata[cname][lineno]) for cname in metadata_colnames]
            templt = ' | '.join([*sent[0], *attrs]) #str(lineno),
            duplicated[templt] += 1
            j = j + 1
            
        #duplicated = sorted([(c,t) for (t,c) in duplicated.items()], reverse=True) # NOTE this makes the line numbers wrong
        duplicated = [(c,t) for (t,c) in duplicated.items()]    # So don't sort it for now

        for count,templt in duplicated:
            #print(f'| {templt} | {count} | {count/total_data_len:.3f} |')
            try:
                print(f'| {templt} |')
            except Exception:
                pass
            
        print()
        # Distribution of some metadata_colnames using this template        
        if len(some_cnames) > 0:
            print(f'### Distribution of {", ".join(some_cnames)} using this template')
            for cname in some_cnames:
                stype_counts = Counter([metadata[cname][lineno] for (_, lineno) in sents])
                solution_types = [stype for stype, count in sorted(list(stype_counts.items()), key=lambda x: -x[1])]

                _print_md_col_names(solution_types)
                row = '| '
                for stype in solution_types:
                    row += f"{str(stype_counts[stype])} ({stype_counts[stype]/N:.3f}) |"
                print(row)
                print()
            

    
    print()


def top_template_phrase_examples(top_temps, state2phrases, k=5, n_phrases=10):
    """
    Parameters
    -----------
        n_phrases:  int
            Print top {n_phrases} examples for each state
    """
    def _print_it(with_freq):
        for template_it in range(k):    # Top 5 templates
            print(f"### Top-{template_it+1}")

            _print_md_col_names(top_temps[template_it])

            template = top_temps[template_it]  # a tuple of states
            template_examples = [[] for i in range(n_phrases)]  #[['phr1-1','phr2-1'], ['ph1-2', 'phr2-2']]
            for i_state,state in enumerate(template):
                # [0] for phrase; [1] for frequency
                phr_frq = sorted(zip(state2phrases[state][1],state2phrases[state][0]), reverse=True)
                for i_exp in range(n_phrases):
                    example_phrase = ' '
                    if i_exp < len(phr_frq):
                        example_phrase = f"{phr_frq[i_exp][1]}"             #e.g. "How much"
                        if with_freq:
                            example_phrase += f" ({phr_frq[i_exp][0]:.2f})"  #e.g. "How much (0.03)"
                    template_examples[i_exp].append(example_phrase)
                    
            for i_exp in range(n_phrases):
                print(f"| {' | '.join(template_examples[i_exp])} |")
            print()

    print(f"# Top {k} templates consist of")
    print(f"## No frequencies")
    _print_it(False)
    print(f"## With frequencies")
    _print_it(True)
    

