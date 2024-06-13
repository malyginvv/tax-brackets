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
    gdp: int
    country_name: str
    currency: str
    source_url: str
    tax_brackets: list

    def convert(self, exchange_rate: float):
        return TaxationData(self.gdp,
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
    gdp: int

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
    'CAD': 1.38,
    'MXN': 18.73,
    'AUD': 1.51,
    'KRW': 1376.55,
    'IDR': 16284.35,
    'TRY': 32.54,
    'CHF': 0.89,
    'PLN': 4.05
}

# Tax brackets in local currency
taxation_data_local = [
    TaxationData(25462700,
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
    TaxationData(17963171,
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
    TaxationData(4072192,
                 'Germany',
                 'EUR',
                 'https://taxsummaries.pwc.com/germany/individual/taxes-on-personal-income',
                 [TaxBracket(0, 0),
                  TaxBracket(11604, 14, True),
                  TaxBracket(66760, 42),
                  TaxBracket(277825, 45)]),
    TaxationData(4231141,
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
    TaxationData(3385090,
                 'India',
                 'INR',
                 'https://taxsummaries.pwc.com/india/individual/taxes-on-personal-income',
                 [TaxBracket(0, 0),
                  TaxBracket(300000, 5),
                  TaxBracket(600000, 10),
                  TaxBracket(900000, 15),
                  TaxBracket(1200000, 20),
                  TaxBracket(1500000, 30)]),
    TaxationData(2240422,
                 'Russia',
                 'RUB',
                 'https://www.banki.ru/news/daytheme/?id=11003233',
                 [TaxBracket(0, 13),
                  TaxBracket(2400000, 15),
                  TaxBracket(5000000, 18),
                  TaxBracket(20000000, 20),
                  TaxBracket(50000000, 22)]),
    TaxationData(3070668,
                 'United Kingdom',
                 'GBP',
                 'https://taxsummaries.pwc.com/united-kingdom/individual/taxes-on-personal-income',
                 [TaxBracket(0, 0),
                  TaxBracket(12570, 20),
                  TaxBracket(50270, 40),
                  TaxBracket(125140, 45)]),
    TaxationData(2782905,
                 'France',
                 'EUR',
                 'https://taxsummaries.pwc.com/france/individual/taxes-on-personal-income',
                 [TaxBracket(0, 0),
                  TaxBracket(11294, 11),
                  TaxBracket(28797, 30),
                  TaxBracket(82341, 41),
                  TaxBracket(177106, 45)]),
    TaxationData(1920096,
                 'Brazil',
                 'BRL',
                 'https://taxsummaries.pwc.com/brazil/individual/taxes-on-personal-income',
                 [TaxBracket(0, 0),
                  TaxBracket(1903.99 * 12, 7.5),
                  TaxBracket(2826.66 * 12, 15),
                  TaxBracket(3751.06 * 12, 22.5),
                  TaxBracket(4664.68 * 12, 27.5)]),
    TaxationData(2010432,
                 'Italy',
                 'EUR',
                 'https://taxsummaries.pwc.com/italy/individual/taxes-on-personal-income',
                 [TaxBracket(0, 23),
                  TaxBracket(28000, 35),
                  TaxBracket(50000, 43)]),
    TaxationData(2139840,
                 'Canada',
                 'CAD',
                 'https://taxsummaries.pwc.com/canada/individual/taxes-on-personal-income',
                 [TaxBracket(0, 15),
                  TaxBracket(53359, 20.5),
                  TaxBracket(106717, 26),
                  TaxBracket(165430, 29),
                  TaxBracket(235675, 33)]),
    TaxationData(1414187,
                 'Mexico',
                 'MXN',
                 'https://taxsummaries.pwc.com/mexico/individual/taxes-on-personal-income',
                 [TaxBracket(0, 1.92),
                  TaxBracket(8952.50, 6.4),
                  TaxBracket(75984.56, 10.88),
                  TaxBracket(133536.08, 16),
                  TaxBracket(155229.81, 17.92),
                  TaxBracket(185852.58, 21.36),
                  TaxBracket(374837.89, 23.52),
                  TaxBracket(590796, 30),
                  TaxBracket(1127926.85, 32),
                  TaxBracket(1503902.47, 34),
                  TaxBracket(4511707.38, 35)]),
    TaxationData(1675419,
                 'Australia',
                 'AUD',
                 'https://taxsummaries.pwc.com/australia/individual/taxes-on-personal-income',
                 [TaxBracket(0, 0),
                  TaxBracket(18200, 19),
                  TaxBracket(45000, 32.5),
                  TaxBracket(120000, 37),
                  TaxBracket(180000, 45)]),
    TaxationData(1665246,
                 'South Korea',
                 'KRW',
                 'https://taxsummaries.pwc.com/republic-of-korea/individual/taxes-on-personal-income',
                 [TaxBracket(0, 6),
                  TaxBracket(14000000, 15),
                  TaxBracket(50000000, 24),
                  TaxBracket(88000000, 35),
                  TaxBracket(150000000, 38),
                  TaxBracket(300000000, 40),
                  TaxBracket(500000000, 42),
                  TaxBracket(1000000000, 45)]),
    TaxationData(1397509,
                 'Spain',
                 'EUR',
                 'https://taxsummaries.pwc.com/spain/individual/taxes-on-personal-income',
                 [TaxBracket(0, 19),
                  TaxBracket(12450, 24),
                  TaxBracket(20200, 30),
                  TaxBracket(35200, 37),
                  TaxBracket(60000, 45),
                  TaxBracket(300000, 47)]),
    TaxationData(1319100,
                 'Indonesia',
                 'IDR',
                 'https://taxsummaries.pwc.com/indonesia/individual/taxes-on-personal-income',
                 [TaxBracket(0, 5),
                  TaxBracket(60000000, 15),
                  TaxBracket(250000000, 25),
                  TaxBracket(500000000, 30),
                  TaxBracket(5000000000, 35)]),
    TaxationData(991115,
                 'Netherlands',
                 'EUR',
                 'https://taxsummaries.pwc.com/netherlands/individual/taxes-on-personal-income',
                 [TaxBracket(0, 9.32),
                  TaxBracket(38098, 36.97),
                  TaxBracket(75518, 49.5)]),
    TaxationData(905988,
                 'Turkey',
                 'TRY',
                 'https://taxsummaries.pwc.com/turkey/individual/taxes-on-personal-income',
                 [TaxBracket(0, 15),
                  TaxBracket(110000, 20),
                  TaxBracket(230000, 27),
                  TaxBracket(870000, 35),
                  TaxBracket(3000000, 40)]),
    # TaxationData(818427,
    #              'Switzerland',
    #              'CHF',
    #              'https://taxsummaries.pwc.com/switzerland/individual/taxes-on-personal-income',
    #              [TaxBracket(0, 15),
    #               TaxBracket(110000, 20),
    #               TaxBracket(230000, 27),
    #               TaxBracket(870000, 35),
    #               TaxBracket(3000000, 40)]),
]


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
                   tax_rates_labels,
                   taxation_data.gdp)


# Tax brackets in USD
taxation_data_usd = list(map(lambda td: td if td.currency == 'USD' else td.convert(exchange_rates[td.currency]),
                             taxation_data_local))

# Bar data
bars = list(map(__to_bars, taxation_data_usd))
