"""
Test nimare.meta.mkda (KDA-based meta-analytic algorithms).
"""
import nimare
from nimare.meta import mkda, kernel
from nimare.correct import FWECorrector, FDRCorrector


def test_mkda_density_kernel_instance_with_kwargs(testdata_cbma):
    """
    Smoke test for MKDADensity with a kernel transformer object, with kernel
    arguments provided, which should result in a warning, but the original
    object's parameters should remain untouched.
    """
    kern = kernel.MKDAKernel(r=2)
    meta = mkda.MKDADensity(kern, kernel__r=6)

    assert meta.kernel_transformer.get_params().get("r") == 2


def test_mkda_density_kernel_class(testdata_cbma):
    """
    Smoke test for MKDADensity with a kernel transformer class.
    """
    meta = mkda.MKDADensity(kernel.MKDAKernel, kernel__r=5)
    res = meta.fit(testdata_cbma)
    assert isinstance(res, nimare.base.MetaResult)


def test_mkda_density_kernel_instance(testdata_cbma):
    """
    Smoke test for MKDADensity with a kernel transformer object.
    """
    kern = kernel.MKDAKernel(r=5)
    meta = mkda.MKDADensity(kern)
    res = meta.fit(testdata_cbma)
    assert isinstance(res, nimare.base.MetaResult)


def test_mkda_density(testdata_cbma):
    """
    Smoke test for MKDADensity
    """
    meta = mkda.MKDADensity()
    res = meta.fit(testdata_cbma)
    corr = FWECorrector(method="montecarlo", voxel_thresh=0.001, n_iters=5, n_cores=1)
    cres = corr.transform(res)
    assert isinstance(res, nimare.base.MetaResult)
    assert isinstance(cres, nimare.base.MetaResult)


def test_mkda_chi2_fdr(testdata_cbma):
    """
    Smoke test for MKDAChi2
    """
    meta = mkda.MKDAChi2()
    res = meta.fit(testdata_cbma, testdata_cbma)
    corr = FDRCorrector(method="bh", alpha=0.001)
    cres = corr.transform(res)
    assert isinstance(res, nimare.base.MetaResult)
    assert isinstance(cres, nimare.base.MetaResult)


def test_mkda_chi2_fwe(testdata_cbma):
    """
    Smoke test for MKDAChi2
    """
    meta = mkda.MKDAChi2()
    res = meta.fit(testdata_cbma, testdata_cbma)
    corr = FWECorrector(method="montecarlo", n_iters=5, n_cores=1)
    cres = corr.transform(res)
    assert isinstance(res, nimare.base.MetaResult)
    assert isinstance(cres, nimare.base.MetaResult)


def test_kda_density(testdata_cbma):
    """
    Smoke test for KDA
    """
    meta = mkda.KDA()
    res = meta.fit(testdata_cbma)
    corr = FWECorrector(method="montecarlo", n_iters=5, n_cores=1)
    cres = corr.transform(res)
    assert isinstance(res, nimare.base.MetaResult)
    assert isinstance(cres, nimare.base.MetaResult)
