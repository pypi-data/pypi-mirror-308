import numpy as np
import pandas as pd
import random
import logging

logger = logging.getLogger("seeder")


class Seeder:
    def __init__(self, df_seeding_population, hourly_probability, scaling_series):
        self.seed_population = None
        self.seed_pattern = None
        self.scaling_series = None

        self.set_seed_population(df_seeding_population)
        self.set_seed_pattern(hourly_probability)
        self.set_sampling_strata(scaling_series)
        return

    def set_sampling_strata(self, scaling_series):
        """
        Takes a pd.Series with a datetime index to scale the seeding probability
        Args:
            scaling_Series (pd.Series): Series with datetime index

        Returns:

        """
        strata_df = pd.DataFrame({"start_date": scaling_series.index,
                                 "scalar": scaling_series})
        strata_df["end_date"] = strata_df["start_date"].shift(-1) - pd.Timedelta(days=1)
        strata_df.loc[strata_df.index[-1], "end_date"] = (strata_df["start_date"].iloc[-1]
                                                          + strata_df["start_date"].diff().median()
                                                          - pd.Timedelta(days=1))
        self.sampling_strata = strata_df
        logger.info(f"Sampling strata set")
        return

    def set_seed_population(self, df_seeding_population):
        """
        Takes a DataFrame with a column "node" and a column "pop" for the information
        which nodes have what seeding population.
        Args:
            df_seeding_population (pd.DataFrame): DataFrame with seeding population.

        Returns:

        """
        self.seed_population = df_seeding_population
        logger.info(f"Seed population set")
        return

    def set_seed_pattern(self, hourly_probability):
        """
        Takes an array with 24 values with the probability of a seed occuring each hour.
        Sum equates to average seeds/day.
        Args:
            hourly_probability (np.array): Array of hourly probabilities.

        Returns:

        """
        self.seed_pattern = hourly_probability
        logger.info(f"Seed pattern set to {hourly_probability}")
        return

    def generate_seeds(self):
        """
        Creates an initial routing table with nodes for columns and each seed is a row with the origin time for the
        origin node. The rest is NaN.
        Args:
            scaling_series (pd.Series): Series with the scaling factor. Index must be DateTime and is used
             for stratification.
            start (pd.Timestamp): Starting timestamp.
            end (pd.Timestamp): Ending timestamp.


        Returns:
            pd.DataFrame: Routing Table with initial seeds.
        """
        ls_seeds = []
        ls_times = []
        # stratified seeding
        for ix, stratum in self.sampling_strata.iterrows():
            # hours during which to create seeds
            hours = pd.date_range(stratum["start_date"], stratum["end_date"], freq='H', inclusive="left")
            # weights for each hour
            hour_weights = stratum["scalar"] * np.array([self.seed_pattern[hour.hour] for hour in hours])
            # create list of seeds from the nodes
            seeds = random.choices(self.seed_population["node"], weights=self.seed_population["pop"],
                                   k=np.around(self.seed_population["pop"].sum() * sum(hour_weights)).astype(int))
            # choose an origin hour for each seed
            seed_hours = [random.choices(hours, hour_weights)[0] for _ in seeds]
            # choose a random time within the hour for each seed
            seed_times = [seed_hour + pd.to_timedelta(random.randint(0, 3599), unit='s') for seed_hour in seed_hours]
            ls_seeds += seeds
            ls_times += seed_times

        seeds = pd.DataFrame.from_dict({"nodes": ls_seeds,
                                        "times": ls_times}).pivot(columns='nodes').droplevel(0, axis=1)
        logger.info(f"{len(seeds)} seeds created for {len(seeds.columns)} nodes "
                    f"between {seeds.min().min():'%Y-%m-%d'} and {seeds.max().max()}:'%Y-%m-%d'")
        return seeds

def main():
    n_years = 5
    seed_pat = pd.Series(0.1 * np.array([1.4, 0.3, 0.1, 0.0, 0.3, 1.7, 9.1, 21, 13, 9, 6.9, 4.9,
                                         1.9, 3.6, 2.5, 2, 2.9, 2.3, 4.1, 4.0, 2.7, 2.1, 2.2, 2.0]) / 100)
    strata_index = pd.date_range('2018-01-01', periods=n_years, freq='YS')
    scaling_series = pd.Series([1.056**a for a in range(n_years)], index=strata_index)
    df_pop = pd.DataFrame({"pop":[100, 150], "node":["NodeA", "NodeB"]})
    seeder = Seeder(df_pop, seed_pat, scaling_series)
    seeds = seeder.generate_seeds()
    return


if __name__ == "__main__":
    main()
    pass
