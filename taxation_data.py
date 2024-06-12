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
    tax_rates_labels: list

    def colors(self, color_mapper):
        return list(map(color_mapper, self.tax_rates))

    def max_tax_rate(self):
        return max(self.tax_rates)

    def avg_tax_rate(self):
        return sum(self.tax_rates) / len(self.tax_rates)


# USD -> Local currency FX rates
exchange_rates = {
    'CNY': 7.24,
    'EUR': 0.92,
    'JPY': 156.12,
    'INR': 83.1,
    'RUB': 89.88,
    'GBP': 0.78,
    'BRL': 5.35,
    'CAD': 1.38
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
                  TaxBracket(960000, 45)]),
    TaxationData('DE',
                 'Germany',
                 'EUR',
                 'https://taxsummaries.pwc.com/germany/individual/taxes-on-personal-income',
                 [TaxBracket(0, 0),
                  TaxBracket(11604, 14, True),
                  TaxBracket(66760, 42),
                  TaxBracket(277825, 45)]),
    TaxationData('JP',
                 'Japan',
                 'JPY',
                 'https://taxsummaries.pwc.com/japan/individual/taxes-on-personal-income',
                 [TaxBracket(0, 5),
                  TaxBracket(1950000, 10),
                  TaxBracket(3300000, 20),
                  TaxBracket(6950000, 23),
                  TaxBracket(9000000, 33),
                  TaxBracket(18000000, 40),
                  TaxBracket(40000000, 45)]),
    TaxationData('IN',
                 'India',
                 'INR',
                 'https://taxsummaries.pwc.com/india/individual/taxes-on-personal-income',
                 [TaxBracket(0, 0),
                  TaxBracket(300000, 5),
                  TaxBracket(600000, 10),
                  TaxBracket(900000, 15),
                  TaxBracket(1200000, 20),
                  TaxBracket(1500000, 30)]),
    TaxationData('RU',
                 'Russia',
                 'RUB',
                 'https://www.banki.ru/news/daytheme/?id=11003233',
                 [TaxBracket(0, 13),
                  TaxBracket(2400000, 15),
                  TaxBracket(5000000, 18),
                  TaxBracket(20000000, 20),
                  TaxBracket(50000000, 22)]),
    TaxationData('UK',
                 'UK',
                 'GBP',
                 'https://taxsummaries.pwc.com/united-kingdom/individual/taxes-on-personal-income',
                 [TaxBracket(0, 0),
                  TaxBracket(12570, 20),
                  TaxBracket(50270, 40),
                  TaxBracket(125140, 45)]),
    TaxationData('FR',
                 'France',
                 'EUR',
                 'https://taxsummaries.pwc.com/france/individual/taxes-on-personal-income',
                 [TaxBracket(0, 0),
                  TaxBracket(11294, 11),
                  TaxBracket(28797, 30),
                  TaxBracket(82341, 41),
                  TaxBracket(177106, 45)]),
    TaxationData('BR',
                 'Brazil',
                 'BRL',
                 'https://taxsummaries.pwc.com/brazil/individual/taxes-on-personal-income',
                 [TaxBracket(0, 0),
                  TaxBracket(1903.99 * 12, 7.5),
                  TaxBracket(2826.66 * 12, 15),
                  TaxBracket(3751.06 * 12, 22.5),
                  TaxBracket(4664.68 * 12, 27.5)]),
    TaxationData('IT',
                 'Italy',
                 'EUR',
                 'https://taxsummaries.pwc.com/italy/individual/taxes-on-personal-income',
                 [TaxBracket(0, 23),
                  TaxBracket(28000, 35),
                  TaxBracket(50000, 43)]),
    TaxationData('CA',
                 'Canada',
                 'CAD',
                 'https://taxsummaries.pwc.com/canada/individual/taxes-on-personal-income',
                 [TaxBracket(0, 15),
                  TaxBracket(53359, 20.5),
                  TaxBracket(106717, 26),
                  TaxBracket(165430, 29),
                  TaxBracket(235675, 33)]),
    TaxationData('PT',
                 'Portugal',
                 'EUR',
                 'https://taxsummaries.pwc.com/portugal/individual/taxes-on-personal-income',
                 [TaxBracket(0, 13.25),
                  TaxBracket(7703, 18),
                  TaxBracket(11623, 23),
                  TaxBracket(16472, 26),
                  TaxBracket(21321, 32.75),
                  TaxBracket(27146, 37),
                  TaxBracket(39791, 43.5),
                  TaxBracket(51997, 45),
                  TaxBracket(81199, 48)]),
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
    tax_rates_labels = []
    for current, following in zip(brackets, brackets[1:]):
        starts.append(current.start)
        widths.append(following.start - current.start)
        tax_rates.append((following.tax_rate + current.tax_rate) // 2 if current.linear else current.tax_rate)
        tax_rates_labels.append(f'{current.tax_rate}-{following.tax_rate}' if current.linear else f'{current.tax_rate}')
    return BarData(taxation_data.country_name,
                   taxation_data.currency,
                   taxation_data.source_url,
                   starts,
                   widths,
                   tax_rates,
                   tax_rates_labels)


# Tax brackets in USD
taxation_data_usd = list(map(lambda td: td if td.currency == 'USD' else td.convert(exchange_rates[td.currency]),
                             taxation_data_local))

# Bar data
bars = list(map(__to_bars, taxation_data_usd))
