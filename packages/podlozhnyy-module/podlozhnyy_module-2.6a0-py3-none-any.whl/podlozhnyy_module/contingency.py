import math
from functools import wraps
from multiprocessing import Process, Queue
from typing import Literal, Optional

from scipy.stats import chi2_contingency, fisher_exact

from podlozhnyy_module import np


def nxm_fisher_exact_test(table: list[list]) -> float:
    """
    Performs Fisher's exact test for a contingency table of an arbitrary size.

    Parameters
    ----------
    table: list[list] or any list alike, e.g. np.ndarray
        contingency matrix M x N

    Returns
    -------
    p-value: float
    """
    num_rows = len(table)
    num_cols = len(table[0])

    row_sums = [sum(row) for row in table]
    col_sums = [sum(table[i][j] for i in range(num_rows)) for j in range(num_cols)]

    log_p_constant = (
        sum(math.lgamma(x + 1) for x in row_sums)
        + sum(math.lgamma(y + 1) for y in col_sums)
        - math.lgamma(sum(row_sums) + 1)
    )

    def calculate_log_probability(contingency_table: list[list]) -> float:
        """
        Calculates the log-probability of a contingency table n x m.

        Fisher's statistic under the truthful null hypothesis has a
        hypergeometric distribution of the numbers in the cells of the table.

        Therefore, the probability of the contingency table follows
        hypergeometric probability mass function $C^K_k * C^N-K_n-k / C^N_n$

        So, simplifying, it's clear that the probability follows:
        the product of factorials of total row and total columns counts
        divided by the total count factorial and factorials of each cell count.

        row_1! x..x row_n! x col_1! x..x col_m! / (cell_11! x..x cell_nm! x total!)

        1. As the gamma function satisfies: gamma(n + 1) = n!
        and it's computationally more stable- it's used instead of factorials.

        2. Making the computations more stable I'm switching from product to sum
        using logarithmic probability.
        """
        return log_p_constant - sum(
            math.lgamma(cell + 1) for row in contingency_table for cell in row
        )

    log_p_obs = calculate_log_probability(table)
    p_value = 0

    def dfs(contingency_table: list[list], row_id, col_id, tol=1e-10):
        """
        Recursive deep-first search function

        Generates all possible contingency tables and calculates their
        log-probability adding up those, that are at least as extreme as
        the observed contingency table, to the total p-value

        Args:
            contingency_table: A list of lists representing the contingency table
            row_id: Row index up to which the table is already filled
            col_id: Column index up to which the table is already filled
            tol: Maximum absolute log-probability comparison error

        Returns:
            None
        """
        nonlocal p_value

        # Copy is necessary to make recursion working
        matrix = [row.copy() for row in contingency_table]

        # Stopping condition - only the last row and column are left
        if row_id == num_rows - 1 and col_id == num_cols - 1:

            for i in range(row_id):  # fill last column
                matrix[i][col_id] = row_sums[i] - sum(matrix[i][:col_id])
            for j in range(col_id):  # fill last row
                matrix[row_id][j] = col_sums[j] - sum(
                    matrix[i][j] for i in range(row_id)
                )

            bottom_right_cell = row_sums[row_id] - sum(matrix[row_id][:col_id])

            if bottom_right_cell < 0:
                # Non-reliable table, all cells must be non-negative
                return

            else:
                matrix[row_id][col_id] = bottom_right_cell
                log_p = calculate_log_probability(matrix)

                if log_p <= log_p_obs + tol:
                    p_value += math.exp(log_p)

                return

        # Fill the table until the Stopping condition isn't met
        else:

            remaining_row_sum = row_sums[row_id] - sum(matrix[row_id])
            remaining_col_sum = col_sums[col_id] - sum(
                matrix[i][col_id] for i in range(num_rows)
            )

            for k in range(min(remaining_row_sum, remaining_col_sum) + 1):

                matrix[row_id][col_id] = k

                if row_id == num_rows - 2 and col_id == num_cols - 2:
                    dfs(matrix, row_id + 1, col_id + 1, tol=tol)
                elif row_id == num_rows - 2:
                    dfs(matrix, 0, col_id + 1, tol=tol)
                else:
                    dfs(matrix, row_id + 1, col_id, tol=tol)

    dfs(contingency_table=[[0] * num_cols for _ in range(num_rows)], row_id=0, col_id=0)

    return p_value


def r_fisher_exact_test(table: np.ndarray) -> float:
    """
    Performs exact Fisher's test using R

    Parameters
    ----------
    table: np.ndarray
        contingency matrix M x N

    Returns
    -------
    p-value: float
    """
    try:
        # Get the packages
        import rpy2.robjects.numpy2ri
        from rpy2.robjects.packages import importr

        # Enable automatic conversion between NumPy and R arrays
        rpy2.robjects.numpy2ri.activate()

        # Import necessary R package
        stats = importr("stats")

        # Perform Fisher's test using the R function with more memory to get p-value
        result = stats.fisher_test(table, workspace=2e9)

        # Extract the p-value
        p_value = result[0][0]

        return p_value

    except ModuleNotFoundError:
        print(
            "The module `rpy2` is not installed properly."
            " Check out the documentation https://rpy2.github.io/doc/v3.5.x/html/overview.html#install-installation"
            " or the thread in https://stackoverflow.com/questions/61622624/how-to-correctly-set-up-rpy2"
            " or simply run the notebook from Jupyter or Google Colab environment."
        )


def subprocess_output(procedure, queue: Optional[Queue] = None):

    @wraps(procedure)
    def wrapper(*args, **kwargs):

        p_value = procedure(*args, **kwargs)
        queue.put(p_value)

        return p_value

    return wrapper


def concurrent_test(
    method: object,
    table: np.ndarray,
    timeout: int = 10,
) -> float:
    """
    Runs the given method in a separate process with a timeout.
    If the process takes longer than the timeout, it is terminated.
    The result is returned from the main process.

    Parameters
    ----------
    method: object
        The method to be run in a separate process.
    table: np.ndarray
        Contingency matrix M x N
    timeout: int
        Time limit for subprocess execution

    Returns
    -------
    p-value: float
    """
    queue = Queue()
    procedure = subprocess_output(method, queue)
    p = Process(target=procedure, args=(table,), name="NxM Fisher's exact test")
    p.start()
    p.join(timeout=timeout)
    p.terminate()
    if p.exitcode is not None:
        p_value = queue.get()
        return p_value


def _contingency_test(table: np.ndarray, criterion: str, timeout: int) -> dict:
    """
    Performs a test of independence of variables in a contingency table

    Parameters
    ----------
    table: np.ndarray
        Contingency matrix M x N
    criterion: str
        Test to be performed
    timeout: int
        Time limit for Fisher's exact test

    Returns
    -------
    dict: {
        "method": str,
        "p-value": float,
        "error": str (optional)
    }
    """
    if criterion not in {"chi-squared", "fisher-exact", "textbook"}:
        raise ValueError(
            "Incorrect type of criterion, "
            "should be one of the following: 'chi-squared', 'fisher-exact', 'textbook'"
        )

    # No timeout if "fisher-exact" criterion is set
    timeout = timeout + 10_000 * (criterion == "fisher-exact")

    result = dict.fromkeys(["method", "p-value"])

    try:
        if criterion == "textbook" and table.shape == (2, 2) and (table >= 10).all():
            result["method"] = "2x2 Pearson's chi-squared test with Yates"
            test = chi2_contingency(table, correction=True)
            result["p-value"] = test.pvalue
        elif criterion != "chi-squared" and table.shape == (2, 2):
            result["method"] = "2x2 Fisher's exact test in Python"
            test = fisher_exact(table)
            result["p-value"] = test.pvalue
        elif criterion == "chi-squared" or (
            criterion == "textbook" and np.sum(table >= 5) >= np.size(table) * 0.80
        ):
            result["method"] = "NxM Pearson's chi-squared test w/o Yates"
            test = chi2_contingency(table, correction=False)
            result["p-value"] = test.pvalue
        else:  # try Exact fisher test if it doesn't take too much
            if np.size(table) > 10:
                name = "NxM Fisher's exact test in R"
                p_value = concurrent_test(r_fisher_exact_test, table, timeout)
            else:
                name = "NxM Fisher's exact test in Python"
                p_value = concurrent_test(nxm_fisher_exact_test, table, timeout)

            result["method"] = name
            if p_value:
                result["p-value"] = p_value
            else:
                result["method"] = " ".join(
                    [
                        result["method"],
                        "timed out.",
                        "NxM Pearson's chi-squared test approximation applied",
                    ]
                )
                test = chi2_contingency(table, correction=False)
                result["p-value"] = test.pvalue

    except Exception as error:
        result["error"] = f"{error}"

    return result


def _validate_input(table: list[list]) -> np.array:

    try:
        array = np.array(table)
    except ValueError:
        raise ValueError("Contingency table's rows must be of equal length.")

    try:
        array = array.astype(dtype=int)
    except ValueError:
        raise ValueError("All cells must contain integer numbers.")

    if array.ndim != 2:
        raise ValueError("Contingency table must be a 2-dimensional array.")

    if (array < 0).any():
        raise ValueError("All cells must contain non-negative numbers.")

    if array.shape[0] == 2 and np.max(np.min(array, axis=1)) == 0:
        raise ValueError(
            "There are cells with zero expected count. "
            "Expectations must contain only positive numbers."
        )

    return array


def general_contingency_test(
    table: list[list],
    criterion: Literal["textbook", "chi-squared", "fisher-exact"] = "textbook",
    timeout: int = 10,
) -> dict:
    """
    Performs a test of independence of variables in a contingency table

    Parameters
    ----------
    table: list[list]
        matrix M x N,
        where M is the number of compared groups and N is the set of measures
    criterion: str
        If 'textbook' the best practice is applied, oit depends on the `table` which procedure is applied, otherwise an
        explicit inference of Fisher Exact or Chi-Squared test happens for 'fisher-exact' or 'chi-squared' accordingly
    timeout: int
        Time limit for Fisher's exact test,
        if the calculation takes longer chi-squared test is applied instead

    Returns
    -------
    dict: {
        "method": str,
        "p-value": float,
        "error": str (optional)
    }
    """
    return _contingency_test(_validate_input(table), criterion, timeout)
