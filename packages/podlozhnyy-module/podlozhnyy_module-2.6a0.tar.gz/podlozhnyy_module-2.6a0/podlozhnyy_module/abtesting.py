import json
from typing import Union

from scipy.stats import multivariate_t, norm
from scipy.stats import t as student
from typing_extensions import Literal

from podlozhnyy_module import np


class StatTest:
    """
    General class for AB testing criterion

    Parameters
    ----------
    input: str | dict
        Is taken in the format of a dictionary or a string
    groups: str
        experiment variant names
    variant: str
        variant to compute p-value for
    """

    def __init__(
        self, input: Union[str, dict], groups: str, variant: str, **kwargs
    ) -> None:

        if isinstance(input, dict):
            self.data = input
        elif isinstance(input, str):
            self.data = json.loads(input)
        else:
            raise TypeError("Incorrect `input` type, should be str or dict")

        if groups not in self.data.keys():
            raise KeyError(
                "Incorrect `groups` value, "
                f"{groups} list with group names missing from data"
            )
        else:
            self.groups = groups

        if self.data[variant] not in self.data[groups]:
            raise KeyError(
                "Incorrect `variant` value, "
                f"{variant} group is not on the `groups` list"
            )
        else:
            self.variant = variant

        for key, value in kwargs.items():
            if value not in self.data.keys():
                raise KeyError(
                    f"Incorrect `{key}` value, "
                    f"there is no '{value}' metric in provided data"
                )
            if len(self.data[value]) != len(self.data[groups]):
                raise ValueError(
                    f"Length of `{value}` list ({len(self.data[value])}) "
                    f"must coincide with the length of `groups` list ({len(self.data[groups])})"
                )

    def _prepare_data(self, *args) -> None:

        self.names = self.data[self.groups].copy()

        if "control" in self.names:
            self.control_name = "control"
        elif "vdefault" in self.names:
            self.control_name = "vdefault"
        else:
            self.control_name = self.names[0]

        control_index = self.names.index(self.control_name)

        self.control_values = dict()
        self.sample_arrays = dict()

        for key in args:
            array = self.data[key].copy()
            self.control_values[key] = array.pop(control_index)
            self.sample_arrays[key] = np.array(array)

        self.names.remove(self.control_name)

    @property
    def statistic(self) -> np.ndarray:

        # to be identified in subclass
        diff = self.point_estimate
        var = self.variance

        statistic = diff / np.sqrt(var * (1 / self.n_samples + 1 / self.n_control))

        return statistic

    def _calculate_pvalue(self, alternative: str) -> None:

        if alternative not in {"two-sided", "greater", "less"}:
            raise ValueError(
                "Incorrect type of alternative, "
                "should be one of the following: 'two-sided', 'greater', 'less'"
            )

    def groups_results(
        self,
        alternative: Literal["two-sided", "less", "greater"] = "two-sided",
    ) -> dict:
        """
        Returns statistic for the entire set of experiments

        Parameters
        ----------
        alternative: str
            type of the alternative hypothesis
        """
        # to be identified in subclass
        self._prepare_data()

        output = dict.fromkeys(
            [
                "variant",
                "statistic",
                "p-value",
            ]
        )
        output["variant"] = self.names
        output["statistic"] = self.statistic
        output["p-value"] = self._calculate_pvalue(
            output["statistic"],
            alternative,
        )

        return output

    def variant_pvalue(self, **kwargs) -> float:
        """
        Returns p-value for specified `variant`

        Keyword Arguments
        ----------
        alternative: str
            type of the alternative hypothesis
        """

        pvalues = self.groups_results(**kwargs).get("p-value")

        if self.data[self.variant] == self.control_name:
            return None
        elif not isinstance(pvalues, np.ndarray):
            return pvalues
        else:
            return pvalues[self.names.index(self.data[self.variant])]


class ProportionTest(StatTest):
    """
    General class for multivariate testing approach for proportions.
    Measure statistics and p-value for the conversion from `base` to `target`.

    Parameters
    ----------
    input: str | dict
        Is taken in the format of a dictionary or a string identical to:
        '{`variant`: "<name>", `groups`: <list of names>, `base`: <list of numbers>, `target`: <list of numbers>}'
        Where the following convention takes place:
            1. `<name>` is the name of the particular group to get p-value for
            2. `<list of names>` contains the list of all the experiment groups, including control
            3. `<list of numbers>` contains one number per group and ordered in accordance with `<list of names>`
    base: str
        conversion denominator name
    target: str
        conversion numerator name
    groups: str
        experiment variant names
    variant: str
        variant to compute p-value for

    Note: at least two lists of numbers must be provided!
    While it may be an arbitrary higher number of supplied metrics, only those two specified in `base` and `target` are used
    """

    def __init__(
        self, input: Union[str, dict], base: str, target: str, groups: str, variant: str
    ) -> None:

        super().__init__(input, groups, variant, base=base, target=target)

        self.base = base
        self.target = target

    def _prepare_data(self) -> None:

        super()._prepare_data(self.base, self.target)

        self.n_control = self.control_values[self.base]
        self.p_control = self.control_values[self.target]

        self.n_samples = self.sample_arrays[self.base]
        self.p_samples = self.sample_arrays[self.target]

    @property
    def point_estimate(self) -> np.ndarray:
        return self.p_samples / self.n_samples - self.p_control / self.n_control


class Ztest(ProportionTest):
    """
    Z-test approach for proportions.
    Returns statistic and p-value of classical Z-test for the specified variant.
    """

    param_starts_from = ProportionTest.__doc__.find(" " * 4 + "Parameters")
    __doc__ = "\n".join([__doc__, ProportionTest.__doc__[param_starts_from:]])

    @property
    def variance(self) -> np.ndarray:

        P = (self.p_samples + self.p_control) / (self.n_samples + self.n_control)
        variance = P * (1 - P)

        return variance

    def _calculate_pvalue(
        self,
        statistic: np.ndarray,
        alternative: str,
    ) -> np.ndarray:

        super()._calculate_pvalue(alternative)

        if alternative == "two-sided":
            pvalue = 2 * (1 - norm.cdf(np.abs(statistic)))
        elif alternative == "greater":
            pvalue = 1 - norm.cdf(statistic)
        elif alternative == "less":
            pvalue = norm.cdf(statistic)

        return pvalue


class ZDunnett(ProportionTest):
    """
    Dunnett's T-test approach for proportions.
    Returns statistic and p-value of Dunnett's T-test for the specified variant.
    """

    param_starts_from = ProportionTest.__doc__.find(" " * 4 + "Parameters")
    __doc__ = "\n".join([__doc__, ProportionTest.__doc__[param_starts_from:]])

    def _prepare_data(self) -> None:

        super()._prepare_data()

        # control group is included
        self.df = self.n_samples.sum() + self.n_control - self.n_samples.size - 1

        # multivariate student distribution matrix
        self.rho = 1 + self.n_control / self.n_samples
        self.rho = 1 / np.sqrt(self.rho[:, None] * self.rho[None, :])
        np.fill_diagonal(self.rho, 1)

    @property
    def variance(self) -> np.ndarray:

        variance = (
            np.sum(self.p_samples * (1 - self.p_samples / self.n_samples))
            + self.p_control * (1 - self.p_control / self.n_control)
        ) / self.df

        return variance

    def _calculate_pvalue(
        self,
        statistic: np.ndarray,
        alternative: str,
        random_state: int = 2024,
    ) -> np.ndarray:

        super()._calculate_pvalue(alternative)

        mvt = multivariate_t(shape=self.rho, df=self.df, seed=random_state)
        statistic = statistic.reshape(-1, 1)

        if alternative == "two-sided":
            pvalue = 1 - mvt.cdf(np.abs(statistic), lower_limit=-np.abs(statistic))
        elif alternative == "greater":
            pvalue = 1 - mvt.cdf(statistic, lower_limit=-np.inf)
        elif alternative == "less":
            pvalue = 1 - mvt.cdf(np.inf, lower_limit=statistic)

        return pvalue


class MeanTest(StatTest):
    """
    General class for multivariate testing approach for averages.
    Measure statistics and p-value for the metric on the basis of the given means and standard deviations.

    Parameters
    ----------
    input: str | dict
        Is taken in the format of a dictionary or a string identical to:
        '{`variant`: "<name>", `groups`: <list of names>, `nobs`: <list of numbers>, `means`: <list of numbers>, `stds`: <list of numbers>}'
        Where the following convention takes place:
            1. `<name>` is the name of the particular group to get p-value for
            2. `<list of names>` contains the list of all the experiment groups, including control
            3. `<list of numbers>` contains one number per group and ordered in accordance with `<list of names>`
    nobs: str
        sample sizes
    means: str
        list of group averages
    stds: str
        list of sample standard deviations (divided by n - 1)
    groups: str
        experiment variant names
    variant: str
        variant to compute p-value for
    """

    def __init__(
        self,
        input: Union[str, dict],
        nobs: str,
        means: str,
        stds: str,
        groups: str,
        variant: str,
    ) -> None:

        super().__init__(input, groups, variant, nobs=nobs, means=means, stds=stds)

        self.nobs = nobs
        self.means = means
        self.stds = stds

    def _prepare_data(self) -> None:

        super()._prepare_data(self.nobs, self.means, self.stds)

        self.n_control = self.control_values[self.nobs]
        self.m_control = self.control_values[self.means]
        self.s_control = self.control_values[self.stds]

        self.n_samples = self.sample_arrays[self.nobs]
        self.m_samples = self.sample_arrays[self.means]
        self.s_samples = self.sample_arrays[self.stds]

    @property
    def point_estimate(self) -> np.ndarray:
        return self.m_samples - self.m_control


class Ttest(MeanTest):
    """
    T-test approach for means comparisons.
    Returns statistic and p-value of classical (in case of `similar_variance=True`) or Welch T-test for the specified variant.
    """

    param_starts_from = MeanTest.__doc__.find(" " * 4 + "Parameters")
    __doc__ = "\n".join(
        [
            __doc__,
            MeanTest.__doc__[param_starts_from:] + "similar_variance: bool = False",
            " " * 8
            + "set to True if the population deviations differ by more than two times",
        ]
    )

    def __init__(
        self,
        input: Union[str, dict],
        nobs: str,
        means: str,
        stds: str,
        groups: str,
        variant: str,
        similar_variance: bool = False,
    ) -> None:

        super().__init__(input, nobs, means, stds, groups, variant)

        self.similar_variance = similar_variance

    def _prepare_data(self) -> None:

        super()._prepare_data()

        if self.similar_variance:
            self.df = self.n_samples + self.n_control - 2
        else:
            self.df = (
                (
                    self.s_samples**2 / self.n_samples
                    + self.s_control**2 / self.n_control
                )
                ** 2
            ) / (
                (self.s_samples**2 / self.n_samples) ** 2 / (self.n_samples - 1)
                + (self.s_control**2 / self.n_control) ** 2 / (self.n_control - 1)
            )

    @property
    def variance(self) -> np.ndarray:
        if self.similar_variance:
            pooled_variance = (
                (self.n_samples - 1) * self.s_samples**2
                + (self.n_control - 1) * self.s_control**2
            ) / (self.n_samples + self.n_control - 2)
            return pooled_variance
        else:
            welch_variance = (
                self.s_samples**2 / self.n_samples
                + self.s_control**2 / self.n_control
            )
            # to cancel the multiplier in general formula
            factor = 1 / self.n_samples + 1 / self.n_control
            return welch_variance / factor

    def _calculate_pvalue(
        self,
        statistic: np.ndarray,
        alternative: str,
    ) -> np.ndarray:

        super()._calculate_pvalue(alternative)

        if alternative == "two-sided":
            pvalue = 2 * (1 - student.cdf(np.abs(statistic), df=self.df))
        elif alternative == "greater":
            pvalue = 1 - student.cdf(statistic, df=self.df)
        elif alternative == "less":
            pvalue = student.cdf(statistic, df=self.df)

        return pvalue


class TDunnett(MeanTest):
    """
    Dunnett's T-test approach for average comparisons.
    Returns statistic and p-value of Dunnett's T-test for the specified variant.
    """

    param_starts_from = MeanTest.__doc__.find(" " * 4 + "Parameters")
    __doc__ = "\n".join([__doc__, MeanTest.__doc__[param_starts_from:]])

    def _prepare_data(self) -> None:

        super()._prepare_data()

        # control group is included
        self.df = self.n_samples.sum() + self.n_control - self.n_samples.size - 1

        # multivariate student distribution matrix
        self.rho = 1 + self.n_control / self.n_samples
        self.rho = 1 / np.sqrt(self.rho[:, None] * self.rho[None, :])
        np.fill_diagonal(self.rho, 1)

    @property
    def variance(self) -> np.ndarray:

        variance = (
            np.sum((self.n_samples - 1) * self.s_samples**2)
            + (self.n_control - 1) * self.s_control**2
        ) / self.df

        return variance

    def _calculate_pvalue(
        self,
        statistic: np.ndarray,
        alternative: str,
        random_state: int = 2024,
    ) -> np.ndarray:

        super()._calculate_pvalue(alternative)

        mvt = multivariate_t(shape=self.rho, df=self.df, seed=random_state)
        statistic = statistic.reshape(-1, 1)

        if alternative == "two-sided":
            pvalue = 1 - mvt.cdf(np.abs(statistic), lower_limit=-np.abs(statistic))
        elif alternative == "greater":
            pvalue = 1 - mvt.cdf(statistic, lower_limit=-np.inf)
        elif alternative == "less":
            pvalue = 1 - mvt.cdf(np.inf, lower_limit=statistic)

        return pvalue
