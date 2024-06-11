import math
from dataclasses import dataclass


@dataclass
class TaxBracket:
    start: float
    tax_rate: float
    linear: bool = False

    def convert(self, exchange_rate: float):
        return TaxBracket(round(self.start / exchange_rate), self.tax_rate, self.linear)


@dataclass
class TaxationData:
    country_code: str
    country_name: str
    currency: str
    source_url: str
    tax_brackets: list

    def convert(self, exchange_rate: float):
        return TaxationData(self.country_code,
                            self.country_name,
                            self.currency,
                            self.source_url,
                            list(map(lambda x: x.convert(exchange_rate), self.tax_brackets)))


@dataclass
class BarData:
    country_name: str
    currency: str
    source_url: str
    starts: list
    widths: list
    tax_rates: list

    def colors(self, color_mapper):
        return list(map(color_mapper, self.tax_rates))


# USD -> Local currency FX rates
exchange_rates = {
    'CNY': 7.24,
    'EUR': 0.92,
    'JPY': 156.12,
    'INR': 83.1,
    'RUB': 89.88,
    'GBP': 0.78,
}

# Tax brackets in local currency
taxation_data_local = [
    TaxationData('US',
                 'USA',
                 'USD',
                 'https://www.irs.gov/filing/federal-income-tax-rates-and-brackets',
                 [TaxBracket(0, 10),
                  TaxBracket(11000, 12),
                  TaxBracket(44725, 22),
                  TaxBracket(95375, 24),
                  TaxBracket(182100, 32),
                  TaxBracket(231250, 35),
                  TaxBracket(578125, 37)]),
    TaxationData('CN',
                 'China',
                 'CNY',
                 'https://taxsummaries.pwc.com/peoples-republic-of-china/individual/taxes-on-personal-income',
                 [TaxBracket(0, 3),
                  TaxBracket(36000, 10),
                  TaxBracket(144000, 20),
                  TaxBracket(300000, 25),
                  TaxBracket(420000, 30),
                  TaxBracket(660000, 35),
                  TaxBracket(960000, 45)])
]

# Amount of skipped ticks on log scale e.g. 3 means skip 10, 100, 1000 and start from 10000
__SKIP_LOGS = 3


def __usd_to_bar_unit(amount: int) -> float:
    if amount == 0:
        return 0
    return math.log10(amount) - __SKIP_LOGS


def __to_bars(taxation_data: TaxationData) -> BarData:
    # Add new marker tax bracket at the end
    brackets = taxation_data.tax_brackets + [TaxBracket(1000000, 0)]

    # Calculate bar widths and start coordinates
    starts = []
    widths = []
    tax_rates = []
    for current, following in zip(brackets, brackets[1:]):
        starts.append(current.start)
        widths.append(following.start - current.start)
        tax_rates.append(current.tax_rate)
    return BarData(taxation_data.country_name, taxation_data.currency, taxation_data.source_url, starts, widths, tax_rates)


# Tax brackets in USD
taxation_data_usd = list(map(lambda td: td if td.currency == 'USD' else td.convert(exchange_rates[td.currency]),
                             taxation_data_local))

# Bar data
bars = list(map(__to_bars, taxation_data_usd))
