import argparse
from dataclasses import dataclass
from typing import Iterator
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as mticker
import matplotlib
from datetime import date

alt_colors = [
    '#0F9D58', # Green
    '#F4B400', # Yellow
    '#4285F4', # Blue
    '#DB4437', # Red
]
matplotlib.rcParams['font.family'] = 'Roboto'
matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=alt_colors)

@dataclass
class Molecule:
    """ Name and year of first laser cooling of a molecule. """
    name: str
    date: date

diatomics = [
        Molecule(name='SrF', date=date(2010, 9, 19)),
        Molecule(name='YO', date=date(2013, 4, 1)),
        Molecule(name='CaF', date=date(2014, 5, 16)),
		Molecule(name='YbF', date=date(2018, 3, 22)),
		Molecule(name='BaH', date=date(2020, 8, 18)),
		Molecule(name='CaH', date=date(2022, 8, 9)),
		Molecule(name='BaF', date=date(2022, 3, 14)),
		Molecule(name='CaD', date=date(2024, 8, 5)),
]

triatomics = [
    Molecule(name='SrOH', date=date(2017, 4, 24)),
    Molecule(name='YbOH', date=date(2020, 2, 19)),
    Molecule(name='CaOH', date=date(2020, 3, 31)),
]

polyatomics = [
    Molecule(name='CaOCH$_3$', date=date(2020, 9, 11)),
]

def get_args():
    parser = argparse.ArgumentParser(
        description='Display number of laser-cooled molecules over the years.',
    )
    parser.add_argument(
        '--save',
        action='store_true',
        default=False,
    )
    args = parser.parse_args()
    return args


def accumulate_by_year(
    yit: Iterator[int],
    mit: Iterator[Molecule],
) -> list[int]:
    mol_cnt_accumulated = [] 
    out_year = next(yit)
    molecule = next(mit)
    counter = 0
    while True:
        if out_year < molecule.date.year:
            mol_cnt_accumulated += [counter]
            try:
                out_year = next(yit)
            except StopIteration:
                raise RuntimeError("End of years before end of molecules.")
            continue

        counter += 1
        try:
            molecule = next(mit)
        except StopIteration:
            mol_cnt_accumulated += [counter]
            for out_year in yit:
                mol_cnt_accumulated += [counter]
            break
    return mol_cnt_accumulated


def main():
    args = get_args()
    timeline = [
        molecule.date.year for molecule in diatomics + triatomics + polyatomics
    ]

    years = np.arange(
        start=min(timeline)-1,
        stop=max(timeline)+2,
        step=1,
        dtype=int,
    )

    width = 2.5
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

    for pos, molecule in enumerate(diatomics):
        ax.text(
            x=2025,
            y=pos + 0.5,
            s=molecule.name,
            ha='left',
            va='center',
        )
    for pos, molecule in enumerate(triatomics):
        offset = len(diatomics)
        ax.text(
            x=2025,
            y=offset + pos + 0.5,
            s=molecule.name,
            ha='left',
            va='center',
        )
    for pos, molecule in enumerate(polyatomics):
        offset = len(diatomics) + len(triatomics)
        ax.text(
            x=2025,
            y=offset + pos + 0.5,
            s=molecule.name,
            ha='left',
            va='center',
        )

    ax.xaxis.set_label_text('Year')
    ax.yaxis.set_label_text('# of laser-cooled molecules')

    ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True, prune='both'))
    ax.yaxis.set_major_locator(mticker.MaxNLocator(integer=True))
    ax.yaxis.set_minor_locator(mticker.MultipleLocator())

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.grid(
        visible=True,
        which='both',
        axis = 'y',
        color='gray',
        lw=0.2,
        ls=':',
        # alpha='0.5',
    )

    ax.set_xlim(2009, 2025)
    ax.set_ylim(0, len(diatomics + triatomics + polyatomics)+0.2)

    plt.legend()
    if args.save is True:
        fig.savefig('laser_cooled_molecules.pdf')
    else:
        plt.show()

if __name__ == "__main__":
    main()
