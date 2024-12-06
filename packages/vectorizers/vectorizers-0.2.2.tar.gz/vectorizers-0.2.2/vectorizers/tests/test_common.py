from collections import namedtuple
from copy import copy
import pytest
from sklearn.exceptions import NotFittedError
from sklearn.preprocessing import normalize

import scipy.sparse
import numpy as np
import pandas as pd

from vectorizers import TokenCooccurrenceVectorizer
from vectorizers import TimedTokenCooccurrenceVectorizer
from vectorizers import NgramCooccurrenceVectorizer
from vectorizers import MultiSetCooccurrenceVectorizer
from vectorizers import NgramVectorizer
from vectorizers import SkipgramVectorizer
from vectorizers import DistributionVectorizer
from vectorizers import HistogramVectorizer
from vectorizers import KDEVectorizer
from vectorizers import LabelledTreeCooccurrenceVectorizer
from vectorizers import WassersteinVectorizer
from vectorizers import ApproximateWassersteinVectorizer
from vectorizers import SinkhornVectorizer
from vectorizers import LZCompressionVectorizer
from pynndescent.distances import cosine

from vectorizers.ngram_vectorizer import ngrams_of
from vectorizers._vectorizers import find_bin_boundaries
from vectorizers.tree_token_cooccurrence import build_tree_skip_grams
from vectorizers.preprocessing import remove_node
from vectorizers._window_kernels import (
    harmonic_kernel,
    flat_kernel,
)
from vectorizers.utils import summarize_embedding, categorical_columns_to_list

from . import raw_string_data


token_data = (
    (1, 3, 1, 4, 2),
    (2, 1, 2, 3, 4, 1, 2, 1, 3, 2, 4),
    (4, 1, 1, 3, 2, 4, 2),
    (1, 2, 2, 1, 2, 1, 3, 4, 3, 2, 4),
    (3, 4, 2, 1, 3, 1, 4, 4, 1, 3, 2),
    (2, 1, 3, 1, 4, 4, 1, 4, 1, 3, 2, 4),
)

text_token_data = (
    ("foo", "pok", "foo", "wer", "bar"),
    (),
    ("bar", "foo", "bar", "pok", "wer", "foo", "bar", "foo", "pok", "bar", "wer"),
    ("wer", "foo", "foo", "pok", "bar", "wer", "bar"),
    ("foo", "bar", "bar", "foo", "bar", "foo", "pok", "wer", "pok", "bar", "wer"),
    ("pok", "wer", "bar", "foo", "pok", "foo", "wer", "wer", "foo", "pok", "bar"),
    (
        "bar",
        "foo",
        "pok",
        "foo",
        "wer",
        "wer",
        "foo",
        "wer",
        "foo",
        "pok",
        "bar",
        "wer",
    ),
)

text_token_data_ngram = (
    ("wer", "pok", "wer"),
    ("bar", "pok", "wer"),
    ("foo", "pok", "wer"),
)
text_token_data_permutation = (("wer", "pok"), ("bar", "pok"), ("foo", "pok", "wer"))
text_token_data_subset = (("foo", "pok"), ("pok", "foo", "foo"))
text_token_data_new_token = (("foo", "pok"), ("pok", "foo", "foo", "zaz"))
text_token_data_ngram_soln = np.array(
    [
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
    ]
)


mixed_token_data = (
    (1, "pok", 1, 3.1415, "bar"),
    ("bar", 1, "bar", "pok", 3.1415, 1, "bar", 1, "pok", "bar", 3.1415),
    (3.1415, 1, 1, "pok", "bar", 3.1415, "bar"),
    (1, "bar", "bar", 1, "bar", 1, "pok", 3.1415, "pok", "bar", 3.1415),
    ("pok", 3.1415, "bar", 1, "pok", 1, 3.1415, 3.1415, 1, "pok", "bar"),
    ("bar", 1, "pok", 1, 3.1415, 3.1415, 1, 3.1415, 1, "pok", "bar", 3.1415),
)

point_data = [
    np.random.multivariate_normal(
        mean=[0.0, 0.0], cov=[[0.5, 0.0], [0.0, 0.5]], size=50
    ),
    np.random.multivariate_normal(
        mean=[0.5, 0.0], cov=[[0.5, 0.0], [0.0, 0.5]], size=60
    ),
    np.random.multivariate_normal(
        mean=[-0.5, 0.0], cov=[[0.5, 0.0], [0.0, 0.5]], size=80
    ),
    np.random.multivariate_normal(
        mean=[0.0, 0.5], cov=[[0.5, 0.0], [0.0, 0.5]], size=40
    ),
    np.random.multivariate_normal(
        mean=[0.0, -0.5], cov=[[0.5, 0.0], [0.0, 0.5]], size=20
    ),
]

value_sequence_data = [
    np.random.poisson(3.0, size=100),
    np.random.poisson(12.0, size=30),
    np.random.poisson(4.0, size=40),
    np.random.poisson(5.0, size=90),
    np.random.poisson(4.5, size=120),
    np.random.poisson(9.0, size=60),
    np.random.poisson(2.0, size=80),
]

path_graph = scipy.sparse.csr_matrix(
    [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]]
)
path_graph_labels = np.array(["a", "b", "a", "c"])
path_graph_two_out = scipy.sparse.csr_matrix(
    [[0, 1, 1, 0], [0, 0, 1, 1], [0, 0, 0, 1], [0, 0, 0, 0]]
)
unique_labels = np.array(["a", "b", "c", "d"])
shifted_labels = np.array(["b", "c", "d", "e"])
tree_sequence = [(path_graph, unique_labels), (path_graph, shifted_labels)]
label_dictionary = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4}
sub_dictionary = {"a": 0, "b": 1, "c": 2}

seq_tree_sequence = [
    (scipy.sparse.csr_matrix([[0, 1], [0, 0]]), np.array(["wer", "pok"])),
    (scipy.sparse.csr_matrix([[0, 1], [0, 0]]), np.array(["bar", "pok"])),
    (
        scipy.sparse.csr_matrix([[0, 1, 0], [0, 0, 1], [0, 0, 0]]),
        np.array(["foo", "pok", "wer"]),
    ),
]

distributions_data = scipy.sparse.rand(
    100, 1000, format="csr", random_state=42, dtype=np.float64
)
vectors_data = np.random.normal(size=(1000, 150))

distributions_data_list = [np.array(x) for x in distributions_data.tolil().data]
vectors_data_list = [
    np.ascontiguousarray(vectors_data[indices])
    for indices in distributions_data.tolil().rows
]
generator_reference_dist = np.full(16, 1.0 / 16.0)
generator_reference_vectors = (
    np.mean(distributions_data.toarray(), axis=0) @ vectors_data
) + np.random.normal(scale=0.25 * np.mean(np.abs(vectors_data)), size=(16, 150))


random_timed_token_data = (
    (["a", 0.1], ["c", 0.2], ["a", 0.4], ["d", 0.5], ["b", 0.6]),
    (
        ["d", 1.1],
        ["a", 1.3],
        ["a", 1.5],
        ["c", 1.7],
        ["b", 2.0],
        ["d", 2.5],
        ["b", 3.0],
    ),
)

tiny_token_data = (
    (1, 3, 1, 4, 2),
    (4, 1, 1, 3, 2, 4, 2),
)

tiny_multi_token_data = (
    ([1], [3], [1], [4], [2]),
    ([4], [1], [1], [3], [2], [4], [2]),
)

timed_tiny_token_data = [
    [["a", 1], ["c", 2], ["a", 3], ["d", 4], ["b", 5]],
    [["d", 6], ["a", 7], ["a", 8], ["c", 9], ["b", 10], ["d", 11], ["b", 12]],
]

hyperedges = [
    [555, 878, 1833, 5590, 8518],
    [619, 1226, 3908, 6558],
    [172, 1126, 1237, 6877],
    [560, 1244, 4174, 5089, 9558],
    [95, 138, 962, 1011, 3440],
    [695, 2118, 3161],
    [79, 2821, 5916, 6905],
    [133, 5350, 8367],
    [21, 539, 1031, 3412],
    [289, 776, 2730, 4253, 4333, 5452, 6109],
    [2205, 2399, 4198, 8700, 8894],
    [152, 279, 4530, 9108],
    [753, 780, 970, 1439, 3532],
    [399, 481, 1062, 1213, 1251, 1866, 3046, 4674, 6768, 7742, 8673],
    [27, 1519, 8966],
    [228, 697, 2358],
    [1100, 1282, 4249, 5072, 6018, 8089, 8481],
    [88, 167, 951, 974, 2051, 2622, 6244, 9674],
    [194, 2269, 2343],
    [3539, 4141, 4370, 9597],
]


@pytest.mark.parametrize("n_iter", [0, 1, 2])
def test_TokenCooccurrence_window_0(n_iter):
    vertex_vectorizer = MultiSetCooccurrenceVectorizer(
        window_radii=0,
        window_orientations="before",
        normalize_windows=False,
        n_iter=n_iter,
    ).fit([hyperedges])
    assert vertex_vectorizer.cooccurrences_.shape == (97, 97)
    assert vertex_vectorizer.cooccurrences_.nnz == 452


@pytest.mark.parametrize("ngram_behaviour", ["subgrams", "exact"])
def test_ngram_size(ngram_behaviour):
    model = NgramVectorizer(ngram_size=2, ngram_behaviour=ngram_behaviour)
    matrix = model.fit_transform(text_token_data)
    assert matrix.nnz == 43
    if ngram_behaviour == "exact":
        assert matrix.shape == (7, 15)
    if ngram_behaviour == "subgrams":
        assert matrix.shape == (7, 19)


def test_LabeledTreeCooccurrenceVectorizer():
    model = LabelledTreeCooccurrenceVectorizer(
        window_radius=2, window_orientation="after"
    )
    result = model.fit_transform(tree_sequence)
    expected_result = scipy.sparse.csr_matrix(
        np.array(
            [
                [0, 1, 1, 0, 0],
                [0, 0, 2, 2, 0],
                [0, 0, 0, 2, 1],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0],
            ]
        )
    )
    assert np.allclose(result.toarray(), expected_result.toarray())

    result = model.transform(tree_sequence)
    expected_result = scipy.sparse.csr_matrix(
        np.array(
            [
                [0, 1, 1, 0, 0],
                [0, 0, 2, 2, 0],
                [0, 0, 0, 2, 1],
                [0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0],
            ]
        )
    )
    assert np.allclose(result.toarray(), expected_result.toarray())


def test_LabeledTreeCooccurrenceVectorizer_reduced_vocab():
    model = LabelledTreeCooccurrenceVectorizer(
        window_radius=2,
        window_orientation="after",
        token_dictionary=sub_dictionary,
    )
    result = model.fit_transform(tree_sequence)
    assert result.shape == (3, 3)


def test_node_removal():
    graph = scipy.sparse.random(10, 10, 0.1, format="csr")
    graph.data = np.ones_like(graph.data)
    node_to_remove = np.argmax(np.array(graph.sum(axis=0)).T[0])
    graph_less_node = remove_node(graph, node_to_remove, inplace=False)
    with pytest.raises(ValueError):
        graph_less_node = remove_node(graph, node_to_remove, inplace=True)
    inplace_graph = graph.tolil()
    remove_node(inplace_graph, node_to_remove, inplace=True)
    assert (inplace_graph != graph_less_node).sum() == 0

    assert np.all([node_to_remove not in row for row in inplace_graph.rows])
    assert len(inplace_graph.rows[node_to_remove]) == 0

    orig_graph = graph.tolil()
    for i, row in enumerate(orig_graph.rows):
        if node_to_remove in row and i != node_to_remove:
            assert np.all(
                np.unique(np.hstack([row, orig_graph.rows[node_to_remove]]))
                == np.unique(np.hstack([inplace_graph.rows[i], [node_to_remove]]))
            )


def test_build_tree_skip_grams_contract():
    (result_matrix, result_labels) = build_tree_skip_grams(
        token_sequence=path_graph_labels,
        adjacency_matrix=path_graph,
        kernel_function=flat_kernel,
        kernel_args=dict(),
        window_size=2,
    )
    expected_result = scipy.sparse.csr_matrix(
        [[1.0, 1.0, 1.0], [1.0, 0.0, 1.0], [0.0, 0.0, 0.0]]
    )
    assert np.allclose(result_matrix.toarray(), expected_result.toarray())


def test_build_tree_skip_grams_no_contract():
    (result_matrix, result_labels) = build_tree_skip_grams(
        token_sequence=unique_labels,
        adjacency_matrix=path_graph,
        kernel_function=flat_kernel,
        kernel_args=dict([]),
        window_size=2,
    )
    assert np.allclose(result_matrix.toarray(), path_graph_two_out.toarray())
    assert np.array_equal(unique_labels, result_labels)


def test_harmonic_kernel():
    kernel = harmonic_kernel([0, 0, 0, 0])
    assert kernel[0] == 1.0
    assert kernel[-1] == 1.0 / 4.0
    assert kernel[1] == 1.0 / 2.0


def test_flat_kernel():
    kernel = flat_kernel([0] * np.random.randint(2, 10))
    assert np.all(kernel == 1.0)


@pytest.mark.parametrize("min_token_occurrences", [None, 2])
@pytest.mark.parametrize("max_document_frequency", [None, 0.7])
@pytest.mark.parametrize("window_orientation", ["before", "after"])
@pytest.mark.parametrize("window_radius", [2])
@pytest.mark.parametrize("kernel_function", ["geometric"])
@pytest.mark.parametrize("mask_string", [None, "[MASK]"])
@pytest.mark.parametrize("nullify_mask", [False, True])
def test_equality_of_Tree_and_Token_CooccurrenceVectorizers(
    min_token_occurrences,
    max_document_frequency,
    window_radius,
    window_orientation,
    kernel_function,
    mask_string,
    nullify_mask,
):
    tree_model = LabelledTreeCooccurrenceVectorizer(
        window_radius=window_radius,
        window_orientation=window_orientation,
        kernel_function=kernel_function,
        min_occurrences=min_token_occurrences,
        max_tree_frequency=max_document_frequency,
        mask_string=mask_string,
        nullify_mask=nullify_mask and not mask_string is None,
    )
    seq_model = TokenCooccurrenceVectorizer(
        window_radii=window_radius,
        window_orientations=window_orientation,
        kernel_functions=kernel_function,
        min_occurrences=min_token_occurrences,
        max_document_frequency=max_document_frequency,
        mask_string=mask_string,
        normalize_windows=False,
        nullify_mask=nullify_mask and not mask_string is None,
    )
    assert np.allclose(
        tree_model.fit_transform(seq_tree_sequence).toarray(),
        seq_model.fit_transform(text_token_data_permutation).toarray(),
    )
    assert np.allclose(
        tree_model.fit_transform(seq_tree_sequence).toarray(),
        tree_model.transform(seq_tree_sequence).toarray(),
    )
    assert np.allclose(
        seq_model.fit_transform(text_token_data_permutation).toarray(),
        seq_model.transform(text_token_data_permutation).toarray(),
    )


@pytest.mark.parametrize("n_iter", [0, 2])
@pytest.mark.parametrize("n_threads", [1, 2])
@pytest.mark.parametrize("normalize_windows", [False, True])
@pytest.mark.parametrize(
    "kernel_function", [["flat", "flat"], ["geometric", "geometric"]]
)
@pytest.mark.parametrize("max_unique_tokens", [None, 2])
@pytest.mark.parametrize("max_occurrences", [None, 3])
def test_equality_of_CooccurrenceVectorizers(
    n_iter,
    normalize_windows,
    kernel_function,
    n_threads,
    max_unique_tokens,
    max_occurrences,
):
    window_radius = [1, 3]
    window_function = ["fixed", "variable"]

    model1 = TokenCooccurrenceVectorizer(
        window_radii=window_radius,
        n_iter=n_iter,
        kernel_functions=kernel_function,
        window_functions=window_function,
        normalize_windows=normalize_windows,
        n_threads=n_threads,
        max_unique_tokens=max_unique_tokens,
        mask_string="m",
        max_occurrences=max_occurrences,
    )
    model2 = TimedTokenCooccurrenceVectorizer(
        window_radii=window_radius,
        kernel_functions=kernel_function,
        window_functions=window_function,
        n_iter=n_iter,
        normalize_windows=normalize_windows,
        n_threads=n_threads,
        max_unique_tokens=max_unique_tokens,
        mask_string="m",
        max_occurrences=max_occurrences,
    )
    model3 = MultiSetCooccurrenceVectorizer(
        window_radii=window_radius,
        kernel_functions=kernel_function,
        window_functions=window_function,
        n_iter=n_iter,
        normalize_windows=normalize_windows,
        n_threads=n_threads,
        max_unique_tokens=max_unique_tokens,
        mask_string="m",
        max_occurrences=max_occurrences,
    )
    base_result = model1.fit_transform(tiny_token_data).toarray()
    assert np.allclose(
        base_result,
        model2.fit_transform(timed_tiny_token_data).toarray(),
    )
    assert np.allclose(
        base_result,
        model3.fit_transform(tiny_multi_token_data).toarray(),
    )
    assert np.allclose(
        base_result,
        model1.transform(tiny_token_data).toarray(),
    )
    assert np.allclose(
        base_result,
        model2.transform(timed_tiny_token_data).toarray(),
    )
    assert np.allclose(
        base_result,
        model3.transform(tiny_multi_token_data).toarray(),
    )


def test_reverse_cooccurrence_vectorizer():
    seq_model1 = TokenCooccurrenceVectorizer(
        window_radii=2,
        window_orientations="after",
        kernel_functions="harmonic",
        mask_string=None,
        normalize_windows=False,
    )
    seq_model2 = TokenCooccurrenceVectorizer(
        window_radii=2,
        window_orientations="before",
        kernel_functions="harmonic",
        mask_string=None,
        normalize_windows=False,
    )
    reversed_after = (seq_model1.fit_transform(text_token_data).toarray().T,)
    before = (seq_model2.fit_transform(text_token_data).toarray(),)
    assert np.allclose(reversed_after, before)


def test_ngrams_of():
    for ngram_size in (1, 2, 4):
        tokens = np.random.randint(10, size=np.random.poisson(5 + ngram_size))
        ngrams = ngrams_of(tokens, ngram_size)
        if len(tokens) >= ngram_size:
            assert len(ngrams) == len(tokens) - (ngram_size - 1)
        else:
            assert len(ngrams) == 0
        assert np.all(
            [ngrams[i][0] == tokens[i] for i in range(len(tokens) - (ngram_size - 1))]
        )
        assert np.all(
            [
                ngrams[i][-1] == tokens[i + (ngram_size - 1)]
                for i in range(len(tokens) - (ngram_size - 1))
            ]
        )


@pytest.mark.parametrize("skip_grams_size", [2, 3])
@pytest.mark.parametrize("n_iter", [0, 2])
def test_token_cooccurrence_vectorizer_ngrams(skip_grams_size, n_iter):
    vectorizer = NgramCooccurrenceVectorizer(n_iter=n_iter, ngram_size=skip_grams_size)
    result = vectorizer.fit_transform(text_token_data_ngram)
    transform = vectorizer.transform(text_token_data_ngram)
    assert (result != transform).nnz == 0
    if n_iter == 0 and skip_grams_size == 2:
        assert np.allclose(result.toarray(), text_token_data_ngram_soln)


def test_token_cooccurrence_vectorizer_window_args():
    vectorizer_a = TokenCooccurrenceVectorizer(window_functions="variable")
    vectorizer_b = TokenCooccurrenceVectorizer(
        window_functions="variable", window_args={"power": 0.75}
    )
    assert (
        vectorizer_a.fit_transform(token_data) != vectorizer_b.fit_transform(token_data)
    ).nnz == 0


def test_token_cooccurrence_vectorizer_kernel_args():
    vectorizer_a = TokenCooccurrenceVectorizer(
        kernel_functions="geometric",
        mask_string="MASK",
        kernel_args={"normalize": True},
    )
    vectorizer_b = TokenCooccurrenceVectorizer(
        kernel_functions="geometric",
        kernel_args={"normalize": True, "p": 0.9},
        mask_string="MASK",
    )
    assert (
        vectorizer_a.fit_transform(token_data) != vectorizer_b.fit_transform(token_data)
    ).nnz == 0


def test_cooccurrence_vectorizer_epsilon():
    vectorizer_a = TokenCooccurrenceVectorizer(epsilon=0)
    vectorizer_b = TokenCooccurrenceVectorizer(epsilon=1e-11)
    vectorizer_c = TokenCooccurrenceVectorizer(epsilon=1)
    mat1 = normalize(
        vectorizer_a.fit_transform(token_data).toarray(), axis=0, norm="l1"
    )
    mat2 = vectorizer_b.fit_transform(token_data).toarray()
    assert np.allclose(mat1, mat2)
    assert vectorizer_c.fit_transform(token_data).nnz == 0


def test_cooccurrence_vectorizer_coo_mem_limit():
    vectorizer_a = TokenCooccurrenceVectorizer(
        window_functions="fixed",
        n_iter=0,
        coo_initial_memory="1k",
        normalize_windows=False,
    )
    vectorizer_b = TokenCooccurrenceVectorizer(
        window_functions="fixed",
        n_iter=0,
        normalize_windows=False,
    )
    np.random.seed(42)
    data = [[np.random.randint(0, 10) for i in range(100)]]
    mat1 = vectorizer_a.fit_transform(data).toarray()
    mat2 = vectorizer_b.fit_transform(data).toarray()
    assert np.allclose(mat1, mat2)


@pytest.mark.parametrize("kernel_function", ["harmonic", "flat", "geometric"])
def test_token_cooccurrence_vectorizer_offset(kernel_function):
    vectorizer_a = TokenCooccurrenceVectorizer(
        kernel_functions=kernel_function, window_radii=1, normalize_windows=False
    )
    vectorizer_b = TokenCooccurrenceVectorizer(
        kernel_functions=kernel_function, window_radii=2, normalize_windows=False
    )
    vectorizer_c = TokenCooccurrenceVectorizer(
        window_radii=2,
        kernel_functions=kernel_function,
        kernel_args={"offset": 1},
        normalize_windows=False,
    )
    mat1 = (
        vectorizer_a.fit_transform(token_data) + vectorizer_c.fit_transform(token_data)
    ).toarray()
    mat2 = vectorizer_b.fit_transform(token_data).toarray()
    assert np.allclose(mat1, mat2)


def test_token_cooccurrence_vectorizer_orientation():
    vectorizer = TokenCooccurrenceVectorizer(
        window_radii=1, window_orientations="directional", normalize_windows=False
    )
    result = vectorizer.fit_transform(text_token_data)
    assert result.shape == (4, 8)
    # Check the pok preceded by wer value is 1
    row = vectorizer.token_label_dictionary_["pok"]
    col = vectorizer.column_label_dictionary_["pre_0_wer"]
    assert result[row, col] == 1
    result_before = TokenCooccurrenceVectorizer(
        window_radii=1, window_orientations="before", normalize_windows=False
    ).fit_transform(text_token_data)
    result_after = TokenCooccurrenceVectorizer(
        window_radii=1, window_orientations="after", normalize_windows=False
    ).fit_transform(text_token_data)
    assert np.all(result_after.toarray() == (result_before.transpose()).toarray())
    assert np.all(
        result.toarray() == np.hstack([result_before.toarray(), result_after.toarray()])
    )


def test_token_cooccurrence_vectorizer_column_order():
    vectorizer = TokenCooccurrenceVectorizer().fit(text_token_data)
    vectorizer_permuted = TokenCooccurrenceVectorizer().fit(text_token_data_permutation)
    assert (
        vectorizer.token_label_dictionary_
        == vectorizer_permuted.token_label_dictionary_
    )


def test_token_cooccurence_vectorizer_transform_new_vocab():
    vectorizer = TokenCooccurrenceVectorizer()
    result = vectorizer.fit_transform(text_token_data_subset)
    transform = vectorizer.transform(text_token_data_new_token)
    assert (result != transform).nnz == 0


def test_token_cooccurrence_vectorizer_fixed_tokens():
    vectorizer = TokenCooccurrenceVectorizer(token_dictionary={1: 0, 2: 1, 3: 2})
    result = vectorizer.fit_transform(token_data)
    assert scipy.sparse.issparse(result)
    vectorizer = TokenCooccurrenceVectorizer(
        window_radii=1, window_orientations="after", normalize_windows=False
    )
    result = vectorizer.fit_transform(token_data)
    assert result[0, 2] == 8
    assert result[1, 0] == 6


def test_token_cooccurrence_vectorizer_excessive_prune():
    vectorizer = TokenCooccurrenceVectorizer(min_frequency=1.0)
    with pytest.raises(ValueError):
        result = vectorizer.fit_transform(token_data)


def test_token_cooccurrence_vectorizer_max_unique_tokens():
    vectorizer = TokenCooccurrenceVectorizer(max_unique_tokens=2)
    vectorizer.fit(token_data)
    assert vectorizer.token_label_dictionary_ == {1: 0, 2: 1}


def test_token_cooccurrence_vectorizer_variable_window():
    vectorizer = TokenCooccurrenceVectorizer(window_functions="variable")
    result = vectorizer.fit_transform(token_data)
    assert scipy.sparse.issparse(result)
    vectorizer = TokenCooccurrenceVectorizer(
        window_radii=1, window_orientations="after", normalize_windows=False
    )
    result = vectorizer.fit_transform(token_data)
    assert result[0, 2] == 8
    assert result[1, 0] == 6


def test_token_cooccurrence_vectorizer_mixed():
    vectorizer = TokenCooccurrenceVectorizer()
    with pytest.raises(ValueError):
        vectorizer.fit_transform(mixed_token_data)


def test_ngram_vectorizer_basic():
    vectorizer = NgramVectorizer()
    result = vectorizer.fit_transform(token_data)
    assert scipy.sparse.issparse(result)
    transform_result = vectorizer.transform(token_data)
    assert np.all(transform_result.data == result.data)
    assert np.all(transform_result.tocoo().col == result.tocoo().col)


def test_ngram_vectorizer_text():
    vectorizer = NgramVectorizer(ngram_size=2, ngram_behaviour="subgrams")
    result = vectorizer.fit_transform(text_token_data)
    assert scipy.sparse.issparse(result)
    # Ensure that the empty document has an all zero row
    assert len((result[1, :]).data) == 0


def test_ngram_vectorizer_mixed():
    vectorizer = SkipgramVectorizer()
    with pytest.raises(ValueError):
        vectorizer.fit_transform(mixed_token_data)


def test_ngram_vectorizer_min_doc():
    vectorizer = NgramVectorizer(min_document_occurrences=2)
    count_matrix = vectorizer.fit_transform(text_token_data_permutation)
    assert count_matrix.shape == (3, 2)
    assert np.all(count_matrix.toarray() == np.array([[1, 1], [1, 0], [1, 1]]))


def test_ngram_vectorizer_min_doc_freq():
    vectorizer = NgramVectorizer(min_document_frequency=0.6)
    count_matrix = vectorizer.fit_transform(text_token_data_permutation)
    assert count_matrix.shape == (3, 2)
    assert np.all(count_matrix.toarray() == np.array([[1, 1], [1, 0], [1, 1]]))


def test_ngram_vectorizer_max_doc():
    vectorizer = NgramVectorizer(max_document_occurrences=1)
    count_matrix = vectorizer.fit_transform(text_token_data_permutation)
    assert count_matrix.shape == (3, 2)
    assert np.all(count_matrix.toarray() == np.array([[0, 0], [1, 0], [0, 1]]))


def test_ngram_vectorizer_max_doc_freq():
    vectorizer = NgramVectorizer(max_document_frequency=0.4)
    count_matrix = vectorizer.fit_transform(text_token_data_permutation)
    assert count_matrix.shape == (3, 2)
    assert np.all(count_matrix.toarray() == np.array([[0, 0], [1, 0], [0, 1]]))


def test_ngram_vectorizer_add_not_fitted():
    left = NgramVectorizer().fit(text_token_data)
    assert (left + NgramVectorizer()) is left
    assert (NgramVectorizer() + left) is left


def test_ngram_vectorizer_add():
    left = NgramVectorizer().fit(text_token_data)
    right = NgramVectorizer().fit(text_token_data_new_token)
    third = NgramVectorizer().fit(text_token_data_subset)
    merged = left + right
    truth = NgramVectorizer().fit(text_token_data + text_token_data_new_token)
    assert np.all(
        np.sum(merged._train_matrix, axis=0) == np.sum(truth._train_matrix, axis=0)
    )
    assert merged._train_matrix.nnz == truth._train_matrix.nnz
    merged = merged + third
    truth = NgramVectorizer().fit(
        text_token_data + text_token_data_new_token + text_token_data_subset
    )
    assert np.all(
        np.sum(merged._train_matrix, axis=0) == np.sum(truth._train_matrix, axis=0)
    )
    assert merged._train_matrix.nnz == truth._train_matrix.nnz


# Merging of models is currently unimplemented for ngrams>1.
# Update this test when that feature is added.
def test_ngram_vectorizer_add_ngram_gt_1():
    left = NgramVectorizer(ngram_size=2).fit(text_token_data)
    right = NgramVectorizer(ngram_size=2).fit(text_token_data_new_token)
    with pytest.raises(NotImplementedError):
        combined_model = left + right


def test_skipgram_vectorizer_basic():
    vectorizer = SkipgramVectorizer()
    result = vectorizer.fit_transform(token_data)
    assert scipy.sparse.issparse(result)
    transform_result = vectorizer.transform(token_data)
    assert np.all(transform_result.data == result.data)
    assert np.all(transform_result.tocoo().col == result.tocoo().col)


def test_skipgram_vectorizer_max_doc():
    vectorizer = SkipgramVectorizer(max_document_occurrences=2)
    count_matrix = vectorizer.fit_transform(text_token_data_permutation)
    assert count_matrix.shape == (3, 1)
    assert np.all(count_matrix.toarray() == np.array([[0], [0], [1]]))


def test_skipgram_vectorizer_min_doc():
    vectorizer = SkipgramVectorizer(min_document_occurrences=2)
    count_matrix = vectorizer.fit_transform(text_token_data_permutation)
    assert count_matrix.shape == (3, 2)
    assert np.all(count_matrix.toarray() == np.array([[0, 1], [0, 0], [1, 0]]))


def test_skipgram_vectorizer_text():
    vectorizer = SkipgramVectorizer()
    result = vectorizer.fit_transform(text_token_data)
    assert scipy.sparse.issparse(result)
    # Ensure that the empty document has an all zero row
    assert len((result[1, :]).data) == 0


def test_skipgram_vectorizer_mixed():
    vectorizer = SkipgramVectorizer()
    with pytest.raises(ValueError):
        vectorizer.fit_transform(mixed_token_data)


def test_distribution_vectorizer_basic():
    vectorizer = DistributionVectorizer(n_components=3)
    result = vectorizer.fit_transform(point_data)
    assert result.shape == (len(point_data), 3)
    transform_result = vectorizer.transform(point_data)
    assert np.all(result == transform_result)


def test_distribution_vectorizer_bad_params():
    vectorizer = DistributionVectorizer(n_components=-1)
    with pytest.raises(ValueError):
        vectorizer.fit(point_data)
    vectorizer = DistributionVectorizer(n_components="foo")
    with pytest.raises(ValueError):
        vectorizer.fit(point_data)
    vectorizer = DistributionVectorizer()
    with pytest.raises(ValueError):
        vectorizer.fit(point_data[0])
    vectorizer = DistributionVectorizer()
    with pytest.raises(ValueError):
        vectorizer.fit(
            [np.random.uniform(size=(10, np.random.poisson(10))) for i in range(5)]
        )
    vectorizer = DistributionVectorizer()
    with pytest.raises(ValueError):
        vectorizer.fit(
            [
                [[1, 2, 3], [1, 2], [1, 2, 3, 4]],
                [
                    [1, 2],
                    [
                        1,
                    ],
                    [1, 2, 3],
                ],
            ]
        )


def test_find_bin_boundaries_min():
    data = np.random.poisson(5, size=1000)
    data = np.append(data, [0, 0, 0])
    bins = find_bin_boundaries(data, 10)
    # Poisson so smallest bin should be at 0
    assert bins[0] == 0.0


def test_find_boundaries_all_dupes():
    data = np.ones(100)
    with pytest.warns(UserWarning):
        bins = find_bin_boundaries(data, 10)
        assert len(bins) == 1


def test_histogram_vectorizer_basic():
    vectorizer = HistogramVectorizer(n_components=20)
    result = vectorizer.fit_transform(value_sequence_data)
    assert result.shape == (len(value_sequence_data), 20)
    transform_result = vectorizer.transform(value_sequence_data)
    assert np.all(result == transform_result)


def test_histogram_vectorizer_outlier_bins():
    vectorizer = HistogramVectorizer(n_components=20, append_outlier_bins=True)
    result = vectorizer.fit_transform(value_sequence_data)
    assert result.shape == (len(value_sequence_data), 20 + 2)
    transform_result = vectorizer.transform([[-1.0, -1.0, -1.0, 150.0]])
    assert transform_result[0][0] == 3.0
    assert transform_result[0][-1] == 1.0


def test_kde_vectorizer_basic():
    vectorizer = KDEVectorizer(n_components=20)
    result = vectorizer.fit_transform(value_sequence_data)
    assert result.shape == (len(value_sequence_data), 20)
    transform_result = vectorizer.transform(value_sequence_data)
    assert np.all(result == transform_result)


@pytest.mark.parametrize(
    "method", ["LOT_exact", "LOT_sinkhorn", "HeuristicLinearAlgebra"]
)
def test_wasserstein_vectorizer_basic(method):
    vectorizer = WassersteinVectorizer(random_state=42, method=method)
    result = vectorizer.fit_transform(distributions_data, vectors=vectors_data)
    transform_result = vectorizer.transform(distributions_data, vectors=vectors_data)
    assert np.allclose(result, transform_result, rtol=1e-3, atol=1e-6)


@pytest.mark.parametrize("reference_size", [None, 8])
@pytest.mark.parametrize(
    "method", ["LOT_exact", "LOT_sinkhorn", "HeuristicLinearAlgebra"]
)
def test_wasserstein_vectorizer_reference_specified(method, reference_size):
    vectorizer = WassersteinVectorizer(random_state=42, method=method)
    result = vectorizer.fit_transform(distributions_data, vectors=vectors_data)
    transform_result = vectorizer.transform(distributions_data, vectors=vectors_data)
    assert np.allclose(result, transform_result, rtol=1e-3, atol=1e-6)


@pytest.mark.parametrize(
    "method", ["LOT_exact", "LOT_sinkhorn", "HeuristicLinearAlgebra"]
)
def test_wasserstein_vectorizer_ndarray(method):
    vectorizer = WassersteinVectorizer(random_state=42, method=method)
    np_distribution_data = np.array(distributions_data.todense())
    result = vectorizer.fit_transform(np_distribution_data, vectors=vectors_data)
    transform_result = vectorizer.transform(np_distribution_data, vectors=vectors_data)
    assert np.allclose(result, transform_result, rtol=1e-3, atol=1e-6)


def test_wasserstein_vectorizer_lists():
    vectorizer = WassersteinVectorizer(random_state=42, input_method="lil")

    result = vectorizer.fit_transform(
        distributions_data_list, vectors=vectors_data_list
    )
    transform_result = vectorizer.transform(
        distributions_data_list, vectors=vectors_data_list
    )
    assert np.allclose(result, transform_result, rtol=1e-3, atol=1e-6)


@pytest.mark.parametrize("input_method", ["generator", "lil"])
def test_wasserstein_vectorizer_incompatable_param(input_method):
    with pytest.raises(ValueError):
        vectorizer = WassersteinVectorizer(
            random_state=42, method="HeuristicLinearAlgebra", input_method=input_method
        )


# both generator_n_distributions and generator_vector_dim must be specified for inpute_method='generator'
def test_wasserstein_vectorizer_generator_missing_param():
    with pytest.raises(ValueError):
        WassersteinVectorizer(random_state=42, input_method="generator")
    with pytest.raises(ValueError):
        WassersteinVectorizer(
            random_state=42, input_method="generator", generator_n_distributions=10
        )
    with pytest.raises(ValueError):
        WassersteinVectorizer(
            random_state=42, input_method="generator", generator_vector_dim=10
        )


def test_wasserstein_vectorizer_generators_bad_params():
    distributions_data_generator = (x for x in distributions_data_list)
    vectors_data_generator = (x for x in vectors_data_list)
    vectorizer = WassersteinVectorizer(
        random_state=42,
        input_method="generator",
        generator_n_distributions=distributions_data.shape[0],
        generator_vector_dim=vectors_data.shape[1],
        reference_size=8,
    )
    # no reference vectors
    with pytest.raises(ValueError):
        vectorizer.fit(distributions_data_generator, vectors=vectors_data_generator)

    # bad data type to fit
    with pytest.raises(ValueError):
        vectorizer.fit(distributions_data, vectors=vectors_data)

    # wrong reference_size
    with pytest.raises(ValueError):
        vectorizer.fit(
            distributions_data_generator,
            vectors=vectors_data_generator,
            reference_distribution=generator_reference_dist,
            reference_vectors=generator_reference_vectors,
        )


@pytest.mark.parametrize("reference_distribution", [None, generator_reference_dist])
def test_wasserstein_vectorizer_generators(reference_distribution):
    distributions_data_generator = (x for x in distributions_data_list)
    vectors_data_generator = (x for x in vectors_data_list)
    vectorizer = WassersteinVectorizer(
        random_state=42,
        input_method="generator",
        generator_n_distributions=distributions_data.shape[0],
        generator_vector_dim=vectors_data.shape[1],
    )
    result = vectorizer.fit_transform(
        distributions_data_generator,
        vectors=vectors_data_generator,
        reference_distribution=reference_distribution,
        reference_vectors=generator_reference_vectors,
    )
    # Generators exhaust so must be rebuilt
    distributions_data_generator = (x for x in distributions_data_list)
    vectors_data_generator = (x for x in vectors_data_list)
    transform_result = vectorizer.transform(
        distributions_data_generator,
        vectors=vectors_data_generator,
        n_distributions=distributions_data.shape[0],
        vector_dim=vectors_data.shape[1],
    )
    assert np.allclose(result, transform_result, rtol=1e-3, atol=1e-6)


def test_wasserstein_vectorizer_generators_blockwise():
    distributions_data_generator = (x for x in distributions_data_list)
    vectors_data_generator = (x for x in vectors_data_list)
    vectorizer = WassersteinVectorizer(
        random_state=42,
        input_method="generator",
        memory_size="50k",
        generator_n_distributions=distributions_data.shape[0],
        generator_vector_dim=vectors_data.shape[1],
    )
    result = vectorizer.fit_transform(
        distributions_data_generator,
        vectors=vectors_data_generator,
        reference_distribution=generator_reference_dist,
        reference_vectors=generator_reference_vectors,
    )
    distributions_data_generator = (x for x in distributions_data_list)
    vectors_data_generator = (x for x in vectors_data_list)
    transform_result = vectorizer.transform(
        distributions_data_generator,
        vectors=vectors_data_generator,
    )
    assert np.allclose(result, transform_result, rtol=1e-3, atol=1e-6)


@pytest.mark.parametrize("method", ["LOT_exact", "LOT_sinkhorn"])
def test_wasserstein_vectorizer_blockwise(method):
    vectorizer = WassersteinVectorizer(
        random_state=42, method=method, memory_size="50k"
    )
    result = vectorizer.fit_transform(distributions_data, vectors=vectors_data)
    transform_result = vectorizer.transform(distributions_data, vectors=vectors_data)
    assert np.allclose(result, transform_result, rtol=1e-3, atol=1e-6)


# @pytest.mark.parametrize("metric", [cosine, "euclidean"])
# def test_wasserstein_vectorizer_list_based(metric):
#     lil_data = normalize(distributions_data, norm="l1").tolil()
#     distributions = [np.array(x) for x in lil_data.data]
#     vectors = [vectors_data[x] for x in lil_data.rows]
#     vectorizer = WassersteinVectorizer(random_state=42, input_method='lil', metric=metric)
#     result = vectorizer.fit_transform(distributions, vectors=vectors)
#     transform_result = vectorizer.transform(distributions, vectors=vectors)
#     assert np.allclose(result, transform_result, rtol=1e-3, atol=1e-6)


def test_wasserstein_vectorizer_list_based_blockwise():
    lil_data = normalize(distributions_data, norm="l1").tolil()
    distributions = [np.array(x) for x in lil_data.data]
    vectors = [vectors_data[x] for x in lil_data.rows]
    vectorizer = WassersteinVectorizer(
        random_state=42, input_method="lil", memory_size="50k"
    )
    result = vectorizer.fit_transform(distributions, vectors=vectors)
    transform_result = vectorizer.transform(distributions, vectors=vectors)
    assert np.allclose(result, transform_result, rtol=1e-3, atol=1e-6)


def test_wasserstein_vectorizer_list_compared_to_sparse():
    lil_data = normalize(distributions_data.astype(np.float64), norm="l1").tolil()
    distributions = [np.array(x) for x in lil_data.data]
    vectors = [vectors_data[x] for x in lil_data.rows]
    vectorizer_sparse = WassersteinVectorizer(random_state=42)
    result_sparse = vectorizer_sparse.fit_transform(
        distributions_data, vectors=vectors_data
    )
    vectorizer_list = WassersteinVectorizer(random_state=42, input_method="lil")
    result_list = vectorizer_list.fit_transform(
        distributions,
        vectors=vectors,
        reference_distribution=vectorizer_sparse.reference_distribution_,
        reference_vectors=vectorizer_sparse.reference_vectors_,
    )
    assert np.allclose(result_sparse, result_list, rtol=1e-3, atol=1e-6)


def test_wasserstein_vectorizer_generator_compared_to_sparse():
    distributions_data_generator = (x for x in distributions_data_list)
    vectors_data_generator = (x for x in vectors_data_list)
    vectorizer_sparse = WassersteinVectorizer(random_state=42)
    result_sparse = vectorizer_sparse.fit_transform(
        distributions_data, vectors=vectors_data
    )
    vectorizer_gen = WassersteinVectorizer(
        random_state=42,
        input_method="generator",
        generator_n_distributions=distributions_data.shape[0],
        generator_vector_dim=vectors_data.shape[1],
    )
    result_list = vectorizer_gen.fit_transform(
        distributions_data_generator,
        vectors=vectors_data_generator,
        reference_distribution=vectorizer_sparse.reference_distribution_,
        reference_vectors=vectorizer_sparse.reference_vectors_,
    )
    assert np.allclose(result_sparse, result_list, rtol=1e-3, atol=1e-6)


# TODO: Write a test for a custom callable metric


@pytest.mark.parametrize("input_method", ["generator", "lil"])
def test_wasserstein_based_vectorizer_basic_bad_params(input_method):
    with pytest.raises(NotImplementedError):
        vectorizer = WassersteinVectorizer(
            method="LOT_sinkhorn", input_method=input_method
        )
        vectorizer.fit(distributions_data)

    with pytest.raises(ValueError):
        WassersteinVectorizer(method="not a real algorithm")

    with pytest.raises(ValueError):
        WassersteinVectorizer(input_method="not a real data format")

    with pytest.raises(ValueError):
        vectorizer = WassersteinVectorizer()
        vectorizer.fit(X=distributions_data, vectors=np.array([[1, 2, 3], [2, 3, 4]]))


# Testing incompatable fit types to those that have been specified in the constructor
# TODO: test the transform as well
@pytest.mark.parametrize("max_distribution_size", [256, 5])
@pytest.mark.parametrize("method", ["LOT_exact", "HeuristicLinearAlgebra"])
@pytest.mark.parametrize("input_method", ["spmatrix", "generator", "lil"])
def test_wasserstein_based_vectorizer_bad_params(
    method, input_method, max_distribution_size
):
    with pytest.raises(ValueError):
        vectorizer = WassersteinVectorizer(
            method=method,
            input_method=input_method,
            max_distribution_size=max_distribution_size,
        )
        vectorizer.fit(distributions_data)

    with pytest.raises(ValueError):
        vectorizer = WassersteinVectorizer(method=method, input_method=input_method)
        vectorizer.fit(mixed_token_data, vectors=vectors_data)

    with pytest.raises(ValueError):
        vectorizer = WassersteinVectorizer(method=method, input_method=input_method)
        vectorizer.fit(point_data, vectors=vectors_data)

    distributions_data_generator = (x for x in distributions_data_list)
    vectors_data_generator = (x for x in vectors_data_list)
    with pytest.raises(ValueError):
        vectorizer = WassersteinVectorizer(method=method, input_method=input_method)
        vectorizer.fit(distributions_data_generator, vectors=vectors_data_generator)


@pytest.mark.parametrize("seq_X", [list, tuple])
@pytest.mark.parametrize("seq_vectors", [list, tuple])
def test_wasserstein_lil_different_length_X_vectors(seq_X, seq_vectors):
    with pytest.raises(ValueError):
        WassersteinVectorizer(input_method="lil", method="LOT_exact").fit(
            seq_X(np.array(a) for a in [[1., 1.], [1., 1., 1.], [1., 1., 1.]]),
            vectors=seq_vectors([vectors_data[:2, :], vectors_data[2:2 + 3, :]])
        )


@pytest.mark.parametrize("seq_X", [list, tuple])
@pytest.mark.parametrize("seq_vectors", [list, tuple])
def test_wasserstein_lil_incoherent_X_vectors(seq_X, seq_vectors):
    with pytest.raises(ValueError):
        WassersteinVectorizer(input_method="lil", method="LOT_exact").fit(
            seq_X(np.array(a) for a in [[1., 1.], [1., 1., 1.], [1., 1., 1.]]),
            vectors=seq_vectors([
                vectors_data[:2],
                vectors_data[2:2 + 3],
                vectors_data[5:5 + 4],
            ])
        )


@pytest.mark.parametrize("seq_X", [list, tuple])
@pytest.mark.parametrize("seq_vectors", [list, tuple])
def test_wasserstein_lil_vectors_varying_size(seq_X, seq_vectors):
    with pytest.raises(ValueError):
        WassersteinVectorizer(input_method="lil", method="LOT_exact").fit(
            seq_X(np.array(a) for a in [[1., 1.], [1., 1., 1.], [1., 1., 1.]]),
            vectors=seq_vectors([
                vectors_data[:2],
                vectors_data[2:2 + 3],
                np.hstack([vectors_data[5:5 + 3], np.zeros((3, 1))]),
            ])
        )


@pytest.mark.parametrize("seq_X", [list, tuple])
@pytest.mark.parametrize("seq_vectors", [list, tuple])
def test_wasserstein_lil_weights_non_sequence(seq_X, seq_vectors):
    with pytest.raises(ValueError):
        WassersteinVectorizer(input_method="lil", method="LOT_exact").fit(
            seq_X(np.array(a) for a in [
                np.ones((2, 2)),
                np.ones((3, 2)),
                np.ones((3, 2)),
            ]),
            vectors=seq_vectors([
                vectors_data[:2],
                vectors_data[2:2 + 3],
                vectors_data[5:5 + 3],
            ])
        )


@pytest.mark.parametrize("method", ["LOT_exact", "LOT_sinkhorn"])
def test_wasserstein_based_vectorizer_bad_metrics(method):
    with pytest.raises(ValueError):
        vectorizer = WassersteinVectorizer(method=method, metric="unsupported_metric")
        vectorizer.fit(distributions_data, vectors=vectors_data)

    with pytest.raises(ValueError):
        vectorizer = WassersteinVectorizer(method=method, metric=0.75)
        vectorizer.fit(distributions_data, vectors=vectors_data)


@pytest.mark.parametrize("dense", [True, False])
@pytest.mark.parametrize("include_values", [True, False])
def test_summarize_embedding_list(dense, include_values):
    vect = NgramVectorizer()
    weight_matrix = vect.fit_transform(text_token_data)
    if dense:
        weight_matrix = weight_matrix.todense()
    summary = summarize_embedding(
        weight_matrix, vect.column_index_dictionary_, include_values=include_values
    )
    expectn = namedtuple("Expectn", ["hard", "soft", "length"])
    expected_result = [
        expectn({"foo": 2.0}, {k: 1.0 for k in ["bar", "pok", "wer"]}, 3),
        expectn({}, {}, 0),
        expectn({"bar": 4.0, "foo": 3.0}, {"pok": 2.0, "wer": 2.0}, 3),
        expectn({k: 2.0 for k in ["bar", "foo", "wer"]}, {}, 3),
        expectn({"bar": 4.0, "foo": 3.0}, {"pok": 2.0, "wer": 2.0}, 3),
        expectn({k: 3.0 for k in ["foo", "pok", "wer"]}, {}, 3),
        expectn({"foo": 4.0, "wer": 4.0}, {"bar": 2.0, "pok": 2.0}, 3),
    ]

    if include_values:
        labels, values = summary
    else:
        labels = summary
        values = [[None] * len(ll) for ll in labels]
    for i in range(2 if dense else 0, 7):
        expectation = expected_result[i]
        assert len(labels[i]) == len(values[i]), (
            f"Row {i}: got {len(labels[i])} labels, but {len(values[i])}"
        )
        assert len(labels[i]) == expectation.length, (
            f"Row {i}: expected {expectation.length} summary elements, "
            f"but got {len(values[i])}"
        )
        hard = copy(expectation.hard)
        for label, value in zip(labels[i], values[i]):
            if label in hard:
                value_expected = hard[label]
                del hard[label]
            elif label in expectation.soft:
                value_expected = expectation.soft[label]
            else:
                assert False, (
                    f"Row {i}: got unexpected label {label}; was expecting "
                    f"either of " + ', '.join(
                        expectation.hard.keys() | expectation.soft.keys()
                    )
                )
            if value:
                assert value_expected == value, (
                    f"Row {i}: expected value {hard[label]} for label "
                    f"{label}, but got {value}"
                )

        assert not hard, (
            f"Row {i}: did not get expected labels " + ', '.join(hard.keys())
        )


@pytest.mark.parametrize("dense", [True, False])
@pytest.mark.parametrize("include_values", [True, False])
def test_summarize_embedding_string(dense, include_values):
    vect = NgramVectorizer()
    weight_matrix = vect.fit_transform(text_token_data)
    if dense:
        weight_matrix = weight_matrix.todense()
    summary = summarize_embedding(
        weight_matrix,
        vect.column_index_dictionary_,
        k=2,
        return_type="string",
        include_values=include_values,
    )
    if include_values:
        expected_result = [
            "foo:2.0,wer:1.0",
            "",
            "bar:4.0,foo:3.0",
            "wer:2.0,foo:2.0",
            "bar:4.0,foo:3.0",
            "wer:3.0,pok:3.0",
            "wer:4.0,foo:4.0",
        ]
    else:
        expected_result = [
            "foo,wer",
            "",
            "bar,foo",
            "wer,foo",
            "bar,foo",
            "wer,pok",
            "wer,foo",
        ]
    if dense:
        assert summary[2:7] == expected_result[2:7]
    else:
        assert summary == expected_result


def test_categorical_columns_to_list():
    df = pd.DataFrame(path_graph.todense(), columns=["a", "b", "c", "d"])
    result_list = categorical_columns_to_list(df, ["a", "c"])
    expected_result = [["a:0", "c:0"], ["a:0", "c:1"], ["a:0", "c:0"], ["a:0", "c:0"]]
    assert expected_result == result_list


def test_categorical_column_to_list_bad_param():
    df = pd.DataFrame(path_graph.todense(), columns=["a", "b", "c", "d"])
    with pytest.raises(ValueError):
        categorical_columns_to_list(df, ["a", "c", "foo"])


def test_lzcompression_vectorizer_basic():
    lzc = LZCompressionVectorizer()
    result1 = lzc.fit_transform(raw_string_data)
    result2 = lzc.transform(raw_string_data)
    assert np.allclose(result1.toarray(), result2.toarray())


def test_lzcompression_vectorizer_badparams():
    with pytest.raises(ValueError):
        lzc = LZCompressionVectorizer(max_dict_size=-1)
        lzc.fit(raw_string_data)

    with pytest.raises(ValueError):
        lzc = LZCompressionVectorizer(max_columns=-1)
        lzc.fit(raw_string_data)
