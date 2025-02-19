import argparse
from dataclasses import dataclass
from typing import Iterator
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import numpy as np
import matplotlib.ticker as mticker
import matplotlib
from datetime import date

matplotlib.rcParams['font.family'] = 'Roboto'

natoms_to_color = {
        'diatomics': '#F4B400', # Yellow
        'triatomics': '#0F9D58', # Green
        '>3 atoms': '#4285F4', # Blue
}

@dataclass
class Molecule:
    """ Name and year of first laser cooling of a molecule. """
    name: str
    date: date
    natoms: int

molecules = [
        Molecule(name='SrF', date=date(2010, 9, 19), natoms=2),
        Molecule(name='YO',  date=date(2013, 4,  1), natoms=2),
        Molecule(name='CaF', date=date(2014, 5, 16), natoms=2),
		Molecule(name='YbF', date=date(2018, 3, 22), natoms=2),
		Molecule(name='BaH', date=date(2020, 8, 18), natoms=2),
		Molecule(name='CaH', date=date(2022, 8, 9), natoms=2),
		Molecule(name='BaF', date=date(2022, 3, 14), natoms=2),
		Molecule(name='CaD', date=date(2024, 8, 5), natoms=2),
        Molecule(name='SrOH', date=date(2017, 4, 24), natoms=3),
        Molecule(name='YbOH', date=date(2020, 2, 19), natoms=3),
        Molecule(name='CaOH', date=date(2020, 3, 31), natoms=3),
        Molecule(name='CaOCH$_3$', date=date(2020, 9, 11), natoms=6),
]
molecules.sort(key=lambda molecule: molecule.date)

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
    timeline = [molecule.date.year for molecule in molecules]

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

    total_by_year = accumulate_by_year(
        yit=iter(years),
        mit=iter(molecules),
    )
    
    ax.step(
        x=years,
        y=total_by_year,
        where='post',
        ls='-',
        color='k',
        lw=2,
    )

    for pos, molecule in enumerate(molecules):
        ax.text(
            x=2025.1,
            y=pos + 0.5,
            s=molecule.name,
            ha='left',
            va='center',
        )
        if molecule.natoms == 2:
            category = "diatomics"
        elif molecule.natoms == 3:
            category = "triatomics"
        else:
            category = ">3 atoms"
        ax.fill_between(
            x=[molecule.date.year, years[-1]],
            y1=[pos]*2,
            y2=[pos + 1]*2,
            color=natoms_to_color[category],
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
    ax.set_ylim(0, len(molecules)+0.2)

    handles = list()
    for category, color in natoms_to_color.items():
        patch = mpatch.Patch(
            color=color,
            label=category,
        )
        handles.append(patch)
    ax.legend(handles=handles)

    if args.save is True:
        fig.savefig('laser_cooled_molecules.pdf')
    else:
        plt.show()

if __name__ == "__main__":
    main()
