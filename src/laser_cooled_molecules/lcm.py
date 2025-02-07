import argparse
import matplotlib.pyplot as plt
import numpy as np
from dataclasses import dataclass
from typing import Iterator


@dataclass
class Molecule:
    """ Name and year of first laser cooling of a molecule. """
    name: str
    year: int

diatomics = [
        Molecule(name='SrF', year=2010),
        Molecule(name='YO', year=2013),
        Molecule(name='CaF', year=2016),
]

triatomics = [
    Molecule(name='SrOH', year=2017),
    Molecule(name='YbOH', year=2020),
    Molecule(name='CaOH', year=2020),
]

polyatomics = [
    Molecule(name='CaOMe', year=2020),
]

def get_args():
    parser = argparse.ArgumentParser(
        description='Display number of laser-cooled molecules over the years.',
    )
    args = parser.parse_args()
    return args


def accumulate_by_year(yit: Iterator[int], mit: Iterator[Molecule]):
    mol_cnt_accumulated = [] 
    year = next(yit)
    molecule = next(mit)
    counter = 0
    while True:
        if year < molecule.year:
            mol_cnt_accumulated += [counter]
            try:
                year = next(yit)
            except StopIteration:
                raise RuntimeError("End of years before end of molecules.")
            continue

        counter += 1
        try:
            molecule = next(mit)
        except StopIteration:
            mol_cnt_accumulated += [counter]
            for year in yit:
                mol_cnt_accumulated += [counter]
            break
    return mol_cnt_accumulated


def main():
    get_args()
    year_of_molecules = [
        molecule.year for molecule in diatomics + triatomics + polyatomics
    ]

    years = np.arange(
        start=min(year_of_molecules)-2,
        stop=max(year_of_molecules)+2,
        step=1,
        dtype=int,
    )

    width = 4
    fig = plt.figure(
        figsize=(16/9 * width, width),
        layout='constrained',
    )
    ax = fig.subplots()


    diatomics_by_year = accumulate_by_year(
        yit=iter(years),
        mit=iter(diatomics),
    )
    triatomics_by_year = accumulate_by_year(
        yit=iter(years),
        mit=iter(triatomics),
    )
    polyatomics_by_year = accumulate_by_year(
        yit=iter(years),
        mit=iter(polyatomics),
    )
    di_and_tri_by_year = [
        t + d for t,d in zip(triatomics_by_year, diatomics_by_year)
    ]
    all_by_year = [
        dt + p for dt, p in zip(di_and_tri_by_year, polyatomics_by_year)
    ]
    
    ax.fill_between(
        x=years,
        y1=all_by_year,
        y2=di_and_tri_by_year,
        step='post',
        alpha=0.4,
    )
    ax.fill_between(
        x=years,
        y1=di_and_tri_by_year,
        y2=diatomics_by_year,
        step='post',
        alpha=0.4,
    )
    ax.fill_between(
        x=years,
        y1=diatomics_by_year,
        y2=[0] * len(years),
        step='post',
        alpha=0.4,
    )

    ax.step(
        x=years,
        y=all_by_year,
        where='post',
        label='>3 atoms',
    )
    ax.step(
        x=years,
        y=di_and_tri_by_year,
        where='post',
        label='triatomics',
    )
    ax.step(
        x=years,
        y=diatomics_by_year,
        where='post',
        label='diatomics',
    )

    plt.legend()
    plt.show()
    return

    plt.rcParams['date.converter'] = 'concise'
    plt.rcParams['figure.figsize'] = [4.8 * 16 / 9, 4.8]
    fig = plt.figure(layout='constrained')
    ax = fig.add_axes([0.075, 0.10, 0.7, 0.8])

    years = [i['date'] for i in parsed_data_list]
    ys = [0 for i in parsed_data_list]

    for i, user in enumerate(users):
        color = COLORS[i % len(COLORS)]
        ys = add_user_to_the_plot(ax, years, ys, parsed_data_list, user, color)

    ax.set_ylim([0.0, 1.0])
    ax.set_title('Cluster disk usage')
    fig.legend(loc='center right', frameon=False, reverse=True)
    plt.show()


if __name__ == "__main__":
    main()
