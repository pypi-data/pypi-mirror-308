import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
import astropy.time as astime
import datetime
import pandas as pd
from ..telescopes.telescopes import Telescope
import astropy.units as u
import numpy as np
import matplotlib.dates as md


@dataclass
class WindowPlot():
    def generate_plots(self):
        with plt.ioff():
            fig, ax = plt.subplots(1, figsize=(18, 12))
            self._plot_basic_setting(fig, ax)
            self._plot_twilight(ax)
            self._plot_Moon(ax)
            self._plot_target(ax)
            self._plot_observation(ax)
            self._write_system_parameters(ax)
            
            return fig, ax


    def _plot_basic_setting(self,
                            fig: plt.Figure,
                            ax: plt.Axes):
        """
        Plot basic settings regardless of what planet is plotted.

        Parameters
        ----------
        fig : plt.Figure
            Figure on which to plot on.
        ax : plt.Axes
            Artist on which to plot on.

        Returns
        -------
        None.

        """
        Night = (self.TimeArray.midnight-1*u.day).to_value('datetime')

        ax.set_title(
            f"Transit of {self.row['Planet.Name']} on night: {Night.strftime('%Y%m%d')} at {self.Location.name} with precision on $T_c$ of: {self.Uncertainty.to(u.min):.2f}; Quality: {self.quality}", fontsize=14)

        ax.axhline(
            np.arcsin(1/self.Airmass_limit) * 180/np.pi,
            ls='--', lw=2,
            color='darkred'
        )

        ax.grid(color='black', linestyle='dashed', linewidth=0.3, alpha=1.0)
        xfmt = md.DateFormatter('%d/%m  %H')
        ax.xaxis.set_major_formatter(xfmt)
        fig.autofmt_xdate()
        hours = md.HourLocator()
        ax.xaxis.set_major_locator(hours)

        ax.set_ylim(0, 90)
        ax2 = ax.twinx()
        ax.set_ylabel('Altitude [deg]', color='k')
        ax2.set_ylabel('Airmass', color='k')
        ax2.tick_params('y', colors='k')
        ax2.set_ylim([0, 90])
        ax2.set_yticklabels(['', 5.76, 2.92, 2.00, 1.56,
                            1.31, 1.15, 1.06, 1.02, 1.00])

        ax.set_xlim(self.TimeArray.Sunset,
                    self.TimeArray.Sunrise)

    def _plot_twilight(self,
                       ax: plt.Axes):
        """
        Overplot the twilight area.

        Parameters
        ----------
        ax : plt.Axes
            Artist on which to plot on.

        Returns
        -------
        None.

        """
        ax.fill_between(self.TimeArray.time_array.to_value(format='datetime'),
                        0, 90,
                        self.AltitudeArray.Sun.alt.value < 0,
                        color='blue',
                        alpha=0.3
                        )
        ax.fill_between(self.TimeArray.time_array.to_value(format='datetime'),
                        0, 90,
                        self.AltitudeArray.Sun.alt.value < -18,
                        color='blue',
                        alpha=0.5
                        )
        return

    def _plot_Moon(self,
                   ax: plt.Axes):
        """
        Overplot the Moon position.

        Parameters
        ----------
        ax : plt.Axes
            Artist on which to plot on.

        Returns
        -------
        None.

        """
        ax.plot(self.TimeArray.time_array.to_value(format='datetime'),
                self.AltitudeArray.Moon.alt.value,
                ls='-',
                label='Moon',
                linewidth=2,
                color='yellow',
                alpha=0.7
                )
        return

    def _plot_target(self,
                     ax: plt.Axes):
        """
        Plot the target, highlighting the transit area.

        Parameters
        ----------
        ax : plt.Axes
            Artist on which to plot.

        Returns
        -------
        None.

        """
        ax.plot(self.TimeArray.time_array.to_value(format='datetime'),
                self.AltitudeArray.target.alt.value,
                ls='-',
                label='Target',
                linewidth=4,
                color='red',
                )
        ax.plot(self.TimeArray.time_array[self.Indices.Transit].to_value(format='datetime'),
                self.AltitudeArray.target[self.Indices.Transit].alt.value,
                ls='-',
                label='Target',
                linewidth=10,
                color='red',
                )

        ax.scatter(
            self.TimeArray.time_array[self.Indices.Transit[0][0]].to_value(
                format='datetime'),
            self.AltitudeArray.target[self.Indices.Transit[0][0]].alt.value,
            color='white',
            zorder=999,
            s=200,
        )
        ax.scatter(
            self.TimeArray.time_array[self.Indices.Transit[-1]
                                      [-1]].to_value(format='datetime'),
            self.AltitudeArray.target[self.Indices.Transit[-1][-1]].alt.value,
            color='white',
            zorder=999,
            s=200,
        )

        return

    def _plot_observation(self,
                          ax: plt.Axes):

        # CLEANME
        self.twilight_observation_time = [
                    self.TimeArray.time_array[self.ObservationsTwilight.complete[0]].to_value(
                        format='datetime'),
                    self.TimeArray.time_array[self.ObservationsTwilight.complete[-1]].to_value(
                        format='datetime')
                ]
                
        if len(self.ObservationsFull.complete) != 0:
            ax.fill_between(self.TimeArray.time_array[self.ObservationsFull.complete].to_value(format='datetime'),
                0, 10,
                color='lime',
                alpha=1,
            )

            ax.text((self.TimeArray.time_array[self.ObservationsFull.complete[0]]+30*u.min).to_value(format='datetime'),
                    5,
                    'Observations (no twilight): ' +
                    self.TimeArray.time_array[self.ObservationsFull.complete[0]].to_value(
                        format='datetime').strftime('%H:%M') + ' - ' +
                    self.TimeArray.time_array[self.ObservationsFull.complete[-1]].to_value(
                        format='datetime').strftime('%H:%M'),
                    fontsize=10,
                    )
            
            self.full_observation_time = [
                self.TimeArray.time_array[self.ObservationsFull.complete[0]].to_value(
                    format='datetime'),
                self.TimeArray.time_array[self.ObservationsFull.complete[-1]
                                          ].to_value(format='datetime')
            ]
            self.twilight_full_is_same = (self.full_observation_time == self.twilight_observation_time)
        else:
            self.twilight_full_is_same = False
            
        
        if (((self.FlagsFull.baseline_ingress) or  # Ingress baseline missing
            (self.FlagsFull.baseline_egress) or  # Egress baseline missing
                (not (self.FlagsWindow.visible) and
                 self.FlagsWindow.visible_twilight)) and # Transit into twilight
            not(self.twilight_full_is_same)): # Twilight == Full observations
            
            ax.fill_between(self.TimeArray.time_array[self.ObservationsTwilight.complete].to_value(format='datetime'),
                10, 20,
                color='orange',
                alpha=1,
                zorder=999
            )

            ax.text((self.TimeArray.time_array[self.ObservationsTwilight.complete[0]]+30*u.min).to_value(
                format='datetime'),
                15,
                'Observation (with twilight): ' +
                self.TimeArray.time_array[self.ObservationsTwilight.complete[0]].to_value(
                format='datetime').strftime('%H:%M') + ' - ' +
                self.TimeArray.time_array[self.ObservationsTwilight.complete[-1]].to_value(
                format='datetime').strftime('%H:%M'),
                fontsize=10,
            )

            ax.axvline(self.TimeArray.time_array[self.ObservationsTwilight.complete[0]].to_value(format='datetime'),
                       ls='--',
                       lw=2,
                       color='orange'
                       )
            ax.axvline(self.TimeArray.time_array[self.ObservationsTwilight.complete[-1]].to_value(format='datetime'),
                       ls='--',
                       lw=2,
                       color='orange')


        ax.axvline(self.TimeArray.T1.to_value(format='datetime'),
                   ls='--', lw=2, color='black')
        ax.axvline(self.TimeArray.T4.to_value(format='datetime'),
                   ls='--', lw=2, color='black')
        if len(self.ObservationsFull.complete) != 0:
            ax.axvline(self.TimeArray.time_array[self.ObservationsFull.complete[0]].to_value(
                format='datetime'), ls='--', lw=2, color='lime')
            ax.axvline(self.TimeArray.time_array[self.ObservationsFull.complete[-1]].to_value(
                format='datetime'), ls='--', lw=2, color='lime')

        return

    def _write_system_parameters(self,
                                 ax: plt.Axes):
        """
        Write the system parameters for given system, including Right Ascension, Declination,V magnitude, Moon angle separation, Transit length, Period, ingress and egress timings.

        Parameters
        ----------
        ax : plt.Axes
            DESCRIPTION.

        Returns
        -------
        None.

        """
        from matplotlib import rc

        if self.AltitudeArray.MoonSeparation.value > 45:
            color = 'black'
        elif self.AltitudeArray.MoonSeparation.value > 30:
            color = 'orange'
        else:
            color = 'red'

        format_text = {'style': 'italic',
                       'size': 12
                       }

        text = ax.text(self.TimeArray.Sunset, 97,
                       f"RA: {self.row['Position.RightAscension']:.2f} ",
                       **format_text
                       )

        text = ax.annotate(
            f"DEC: {self.row['Position.Declination']:.2f} ",
            xycoords=text,
            xy=(1, 0), verticalalignment="bottom",
            **format_text
        )

        text = ax.annotate(
            f"; V = {self.row['Magnitude.V']:.3f} ",
            xycoords=text,
            xy=(1, 0), verticalalignment="bottom",
            **format_text
        )
        text = ax.annotate(
            f"; Moon = {self.AltitudeArray.MoonSeparation.value:.0f} deg ",
            xycoords=text,
            xy=(1, 0), verticalalignment="bottom",
            **format_text
        )
        text = ax.annotate(
            '; $T_{14}$' + f" = {self.row['Planet.TransitDuration']:.3f} h ",
            xycoords=text,
            xy=(1, 0), verticalalignment="bottom",
            **format_text
        )

        text = ax.annotate(
            f"; P = {self.row['Planet.Period']:.5f} d ",
            xycoords=text,
            xy=(1, 0), verticalalignment="bottom",
            **format_text
        )

        sunset_text = ax.text(self.TimeArray.Sunset, -10,
                              f"ingress= {self.TimeArray.T1.to_value('datetime').strftime('%H:%M')}",
                              style='italic',
                              bbox=dict(
                                  facecolor='none',
                                  edgecolor='black',
                                  pad=7
                              )
                              )

        sunset_text = ax.annotate(
            (f"Observations (no twilight): {self.TimeArray.time_array[self.ObservationsFull.complete[0]].to_value(format='datetime').strftime('%H:%M')} " +
             f"- {self.TimeArray.time_array[self.ObservationsFull.complete[-1]].to_value(format='datetime').strftime('%H:%M')}"),
            xycoords=sunset_text,
            xy=(1.4, 0), verticalalignment="bottom",
            bbox=dict(
                facecolor='green',
                edgecolor='black',
                boxstyle='round, pad=1'
            )
        )

        if not(self.full_observation_time == self.twilight_observation_time):
            sunset_text = ax.annotate(
                (f"Observation (with twilight): {self.TimeArray.time_array[self.ObservationsTwilight.complete[0]].to_value(format='datetime').strftime('%H:%M')} " +
                f"- {self.TimeArray.time_array[self.ObservationsTwilight.complete[-1]].to_value(format='datetime').strftime('%H:%M')}"),
                xycoords=sunset_text,
                xy=(1.4, 0), verticalalignment="bottom",
                bbox=dict(
                    facecolor='orange',
                    edgecolor='black',
                    boxstyle='round,pad=1'
                ),
            )

        ax.text(self.TimeArray.Sunrise, -10,
                f"egress= {self.TimeArray.T4.to_value('datetime').strftime('%H:%M')}",
                style='italic',
                bbox=dict(
                    facecolor='none',
                    edgecolor='black',
                    pad=7)
                )
        return
