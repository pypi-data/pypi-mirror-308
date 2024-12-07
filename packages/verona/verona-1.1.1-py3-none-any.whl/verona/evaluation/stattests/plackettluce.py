import tempfile
from typing import List, Tuple

import numpy as np
import pandas as pd
from cmdstanpy import CmdStanModel, cmdstan_path, install_cmdstan

from verona.evaluation.stattests.stan_codes import STAN_CODE


class PlackettLuceResults:
    """
    Encapsulates the results from running the Plackett-Luce ranking model.

    This class serves as a container for the results obtained after fitting the Plackett-Luce
    model using MCMC sampling. It provides structured access to important quantities such as
    the expected probabilities, expected ranks, and the posterior distributions of these metrics.

    Attributes:
        expected_prob (pd.Series):
            A pandas Series object representing the expected probabilities for each algorithm.
            It quantifies the estimated likelihood that each algorithm is the best among the ones compared.

        expected_rank (pd.Series):
            A pandas Series object representing the expected ranks for each algorithm.
            The rank is a numerical ordering where lower values indicate better performance.

        posterior (dict or similar container):
            A container (e.g., dictionary) that holds the posterior distributions for the rank
            and probabilities of each algorithm. These distributions capture the uncertainties
            in the point estimates and are essential for Bayesian inference.
    """
    def __init__(self, expected_prob: pd.Series, expected_rank: pd.Series, posterior: pd.DataFrame):
        """
        Initializes the PlackettLuceResults object with the estimated metrics.

        Args:
            expected_prob (pd.Series): Expected probabilities for each algorithm.
            expected_rank (pd.Series): Expected ranks for each algorithm.
            posterior (pd.DataFrame): Posterior distributions for rank and probabilities.

        """
        self.expected_prob = expected_prob
        self.expected_rank = expected_rank
        self.posterior = posterior


class PlackettLuceRanking:

    def __init__(self, result_matrix: pd.DataFrame, approaches: List[str]):
        """
        Parameters:
            result_matrix (pd.DataFrame): Matrix of results in which each row represents a dataset and each column
                represents an algorithm.
            approaches (List[str]): List of the names of approaches in the result matrix
        """
        self.result_matrix = result_matrix
        self.approaches = approaches

        assert (approaches is not None) and (len(approaches) > 0), "The list of approaches is none or empty"
        assert self.result_matrix.shape[1] == len(approaches), "The number of columns in the result matrix does not " \
                                                               "match the approaches specified"

        self.result_matrix.columns = approaches

        try:
            cmdstan_path()
        except:
            install_cmdstan()

    def run(self, n_chains=8, num_samples=300000, mode="max") -> PlackettLuceResults:
        """
        Execute the Plackett-Luce ranking model to estimate the rank and probabilities of each algorithm
        based on their performance metrics.

        The method employs Markov Chain Monte Carlo (MCMC) sampling, leveraging the STAN backend,
        to estimate the posterior distribution of the rank and probabilities.


        Args:
            n_chains (int, optional): Number of chains used ot perform the sampling. Default is ``8``.
            num_samples (int, optional): Number of samples to considerate in the MCMC. Default is ``300000``.
            mode (Literal['max', 'min'], optional): If ``'max'`` the higher the value the better the algorithm.
                If ``'min'`` the lower the value the better the algorithm.
                Default is ``'max'``.

        Returns:
            PlackettLuceResutls : ``PackettLuceResutls`` instance containing:
                - expected_prob: Expected probability of each algorithm having the best ranking
                - expected_rank: Expected rank of each algorithm
                - posterior: Posterior

        Examples:
            >>> result_matrix = pd.DataFrame([[0.75, 0.6, 0.8], [0.8, 0.7, 0.9], [0.9, 0.8, 0.7]])
            >>> plackett_ranking = PlackettLuceRanking(result_matrix, ["a1", "a2", "a3"])
            >>> results = plackett_ranking.run(n_chains=10, num_samples=300000, mode="max")
            >>> print("Expected prob: ", results.expected_prob)
            Expected prob:  a1    0.432793
                            a2    0.179620
                            a3    0.387587
            >>> print("Expected rank: ", results.expected_rank)
            Expected rank:  a1    1.580505
                            a2    2.667531
                            a3    1.751964
        """

        assert mode in ["max", "min"]
        assert n_chains > 0
        assert num_samples > 0

        rank_matrix = self._get_rank_matrix(result_matrix=self.result_matrix, mode=mode)
        stan_result = self._run_stan(rank_matrix=rank_matrix, n_chains=n_chains, num_samples=num_samples)
        expected_prob, expected_rank, posterior = self._get_results_from_stan(stan_results=stan_result)
        self.posterior = posterior
        results = PlackettLuceResults(expected_prob, expected_rank, posterior)
        return results

    def _get_rank_matrix(self, result_matrix: pd.DataFrame, mode="max") -> pd.DataFrame:
        """
        Compute the rank matrix of a matrix of results. If the mode is max, assume that the higher the result,
        the better.
        If the mode is min, do otherwise.

        Args:
            result_matrix (pd.DataFrame): Matrix of results.
            mode (Literal['max', 'min'], optional): ``'max'`` for assigning better ranks to high results.
                ``'min'`` for otherwise.
                Default is ``'max'``.

        Returns:
            rank_matrix : Rank matrix of the result matrix.

        """
        if mode == "min":
            rank_matrix = result_matrix.rank(axis=1, ascending=True)
        else:
            rank_matrix = result_matrix.rank(axis=1, ascending=False)

        rank_matrix = rank_matrix.astype(int)

        return rank_matrix

    def _run_stan(self, rank_matrix, n_chains=8, num_samples=300000) -> pd.DataFrame:
        """
        Execute the STAN program for the Plackett-Luce ranking model.

        Parameters:
            rank_matrix : Matrix of ranks.
            n_chains (int, optional): Number of simulations. Default is ``8``.
            num_samples (int, optional): Number of samples. Default is ``300000``.

        Returns:
            results : Raw results from executing the STAN program.
        """

        stan_code = STAN_CODE.PLACKETT_LUCE_TEST_V3
        rank_matrix = np.array(rank_matrix)
        n = rank_matrix.shape[0]
        m = rank_matrix.shape[1]
        alpha = [1] * m
        weights = [1] * n
        stan_data = {
            "n": n,
            "m": m,
            "ranks": rank_matrix,
            "alpha": alpha,
            "weights": weights
        }

        with tempfile.NamedTemporaryFile(suffix='.stan', delete=False) as temp:
            temp.write(stan_code.encode('utf-8'))
            temp_file_name = temp.name  # Save the filename to use later

        model = CmdStanModel(stan_file=temp_file_name)
        fit = model.sample(data=stan_data, chains=n_chains, iter_sampling=num_samples,
                           iter_warmup=int(num_samples/4), seed=42)

        results = fit.draws_pd()

        import os
        os.remove(temp_file_name)

        return results

    def _get_results_from_stan(self, stan_results) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Extract, parse and beautify the STAN results.

        Parameters
        ----------
        stan_results : Raw stan results.

        Returns
        -------
        expected_prob : Expected probability of each approach to be the best in terms of ranking.
        expected_rank : Expected rank of the approach.
        posterior : Posterior probability, used to calculate the plot.
        """
        columns = [col for col in stan_results.columns if "ratings" in col]
        posterior = stan_results[columns]
        # Set the approaches names so the figure generated has meaningful names
        posterior.columns = self.approaches
        ranks = (posterior * -1).rank(axis=1)
        expected_prob = posterior.mean(axis=0)
        expected_rank = ranks.mean(axis=0)
        return expected_prob, expected_rank, posterior
