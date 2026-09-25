from research.model import normalize_technology,jaccard,compare_pair_sets,validate_bundle
def test_normalization(): assert normalize_technology('Python 3 / NumPy')=='python 3 numpy'
def test_jaccard(): assert jaccard({'a','b'},{'b','c'})==1/3
def test_pair_comparison():
    z=compare_pair_sets({('1','a'),('1','b')},{('1','b'),('1','c')}); assert z['persisted_pairs']==1 and abs(z['global_jaccard']-1/3)<1e-12
def test_packaged_subset(): assert validate_bundle()
