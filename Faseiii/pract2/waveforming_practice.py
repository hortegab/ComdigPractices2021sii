#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: waveforming_practice
# Author: Homero Ortega Boada
# Description: Lo máximo para practicar el tema de Filtro Coseno Alzado
# GNU Radio version: 3.9.5.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from b_FLL_tunner2 import b_FLL_tunner2  # grc-generated hier_block
from b_demod_constelacion_cb import b_demod_constelacion_cb  # grc-generated hier_block
from b_diez_cc import b_diez_cc  # grc-generated hier_block
from b_diezmador_ff import b_diezmador_ff  # grc-generated hier_block
from b_meter_power_cc import b_meter_power_cc  # grc-generated hier_block
from b_upconverter_cf import b_upconverter_cf  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
import numpy
from gnuradio import digital
from gnuradio import fec
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import math
import numpy as np
import random
import waveforming_practice_epy_block_0 as epy_block_0  # embedded python block
import waveforming_practice_wform as wform  # embedded python module



from gnuradio import qtgui

class waveforming_practice(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "waveforming_practice", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("waveforming_practice")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "waveforming_practice")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.constelacion = constelacion = digital.constellation_16qam().points()
        self.Sps = Sps = 8
        self.Rs = Rs = 32000
        self.samp_rate = samp_rate = Rs*Sps
        self.M = M = len(constelacion )
        self.bps = bps = int(math.log(M,2))
        self.Fmax = Fmax = samp_rate/2
        self.retardo_propag = retardo_propag = 1
        self.ntaps = ntaps = 16*Sps
        self.h = h = [1]*Sps
        self.fading = fading = 1
        self.ch_freq = ch_freq = 0
        self.beta = beta = 1
        self.Timing = Timing = 1
        self.Rb = Rb = Rs*bps
        self.Pn = Pn = 0.05
        self.Gain_USRP_Tx_dB = Gain_USRP_Tx_dB = 30.
        self.Gain_USRP_Rx_dB = Gain_USRP_Rx_dB = 20
        self.Delay_eye = Delay_eye = 0
        self.Ch_phase = Ch_phase = 0
        self.BW_filtro = BW_filtro = Fmax

        ##################################################
        # Blocks
        ##################################################
        self.menu = Qt.QTabWidget()
        self.menu_widget_0 = Qt.QWidget()
        self.menu_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.menu_widget_0)
        self.menu_grid_layout_0 = Qt.QGridLayout()
        self.menu_layout_0.addLayout(self.menu_grid_layout_0)
        self.menu.addTab(self.menu_widget_0, 'Time')
        self.menu_widget_1 = Qt.QWidget()
        self.menu_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.menu_widget_1)
        self.menu_grid_layout_1 = Qt.QGridLayout()
        self.menu_layout_1.addLayout(self.menu_grid_layout_1)
        self.menu.addTab(self.menu_widget_1, 'PSD')
        self.menu_widget_2 = Qt.QWidget()
        self.menu_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.menu_widget_2)
        self.menu_grid_layout_2 = Qt.QGridLayout()
        self.menu_layout_2.addLayout(self.menu_grid_layout_2)
        self.menu.addTab(self.menu_widget_2, 'Eye Diagram')
        self.menu_widget_3 = Qt.QWidget()
        self.menu_layout_3 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.menu_widget_3)
        self.menu_grid_layout_3 = Qt.QGridLayout()
        self.menu_layout_3.addLayout(self.menu_grid_layout_3)
        self.menu.addTab(self.menu_widget_3, 'Constellation')
        self.menu_widget_4 = Qt.QWidget()
        self.menu_layout_4 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.menu_widget_4)
        self.menu_grid_layout_4 = Qt.QGridLayout()
        self.menu_layout_4.addLayout(self.menu_grid_layout_4)
        self.menu.addTab(self.menu_widget_4, 'Timing')
        self.menu_widget_5 = Qt.QWidget()
        self.menu_layout_5 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.menu_widget_5)
        self.menu_grid_layout_5 = Qt.QGridLayout()
        self.menu_layout_5.addLayout(self.menu_grid_layout_5)
        self.menu.addTab(self.menu_widget_5, 'M-PAM')
        self.menu_widget_6 = Qt.QWidget()
        self.menu_layout_6 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.menu_widget_6)
        self.menu_grid_layout_6 = Qt.QGridLayout()
        self.menu_layout_6.addLayout(self.menu_grid_layout_6)
        self.menu.addTab(self.menu_widget_6, 'Bits')
        self.menu_widget_7 = Qt.QWidget()
        self.menu_layout_7 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.menu_widget_7)
        self.menu_grid_layout_7 = Qt.QGridLayout()
        self.menu_layout_7.addLayout(self.menu_grid_layout_7)
        self.menu.addTab(self.menu_widget_7, 'RF')
        self.top_grid_layout.addWidget(self.menu, 10, 0, 1, 2)
        for r in range(10, 11):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._retardo_propag_range = Range(0, Sps*ntaps, 1, 1, 200)
        self._retardo_propag_win = RangeWidget(self._retardo_propag_range, self.set_retardo_propag, "Delay_Propagation_Compensation", "counter_slider", int, QtCore.Qt.Horizontal)
        self.menu_grid_layout_4.addWidget(self._retardo_propag_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.menu_grid_layout_4.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_4.setColumnStretch(c, 1)
        self._fading_range = Range(0, 1, 1/100, 1, 200)
        self._fading_win = RangeWidget(self._fading_range, self.set_fading, "fading", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._fading_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._ch_freq_range = Range(0, 100, 1/100, 0, 200)
        self._ch_freq_win = RangeWidget(self._ch_freq_range, self.set_ch_freq, "ch_freq", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._ch_freq_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Timing_range = Range(0, Sps-1, 1, 1, 200)
        self._Timing_win = RangeWidget(self._Timing_range, self.set_Timing, "Timing", "counter_slider", int, QtCore.Qt.Horizontal)
        self.menu_grid_layout_4.addWidget(self._Timing_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.menu_grid_layout_4.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_4.setColumnStretch(c, 1)
        self._Pn_range = Range(0, 1, 1/100, 0.05, 200)
        self._Pn_win = RangeWidget(self._Pn_range, self.set_Pn, "Potencia del ruido", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._Pn_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Delay_eye_range = Range(0, Sps-1, 1, 0, 200)
        self._Delay_eye_win = RangeWidget(self._Delay_eye_range, self.set_Delay_eye, "Centering the Eye", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._Delay_eye_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Ch_phase_range = Range(0, math.pi*2, 1/100, 0, 200)
        self._Ch_phase_win = RangeWidget(self._Ch_phase_range, self.set_Ch_phase, "Ch_phase", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._Ch_phase_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_3 = qtgui.time_sink_f(
            1024, #size
            samp_rate, #samp_rate
            "Power meter (dB)", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_3.set_update_time(0.10)
        self.qtgui_time_sink_x_3.set_y_axis(-20, 6)

        self.qtgui_time_sink_x_3.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_3.enable_tags(True)
        self.qtgui_time_sink_x_3.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_3.enable_autoscale(False)
        self.qtgui_time_sink_x_3.enable_grid(False)
        self.qtgui_time_sink_x_3.enable_axis_labels(True)
        self.qtgui_time_sink_x_3.enable_control_panel(False)
        self.qtgui_time_sink_x_3.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [3, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_3.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_3.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_3.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_3.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_3.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_3.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_3.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_3_win = sip.wrapinstance(self.qtgui_time_sink_x_3.qwidget(), Qt.QWidget)
        self.menu_grid_layout_4.addWidget(self._qtgui_time_sink_x_3_win, 2, 1, 1, 1)
        for r in range(2, 3):
            self.menu_grid_layout_4.setRowStretch(r, 1)
        for c in range(1, 2):
            self.menu_grid_layout_4.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_2_0 = qtgui.time_sink_f(
            32*bps, #size
            Rb, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2_0.set_update_time(0.10)
        self.qtgui_time_sink_x_2_0.set_y_axis(-0.5, 1.5)

        self.qtgui_time_sink_x_2_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2_0.enable_tags(True)
        self.qtgui_time_sink_x_2_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2_0.enable_autoscale(False)
        self.qtgui_time_sink_x_2_0.enable_grid(False)
        self.qtgui_time_sink_x_2_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_2_0.enable_control_panel(False)
        self.qtgui_time_sink_x_2_0.enable_stem_plot(True)


        labels = ['t4', 'r4', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [3, 3, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, 0, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_0_win = sip.wrapinstance(self.qtgui_time_sink_x_2_0.qwidget(), Qt.QWidget)
        self.menu_grid_layout_6.addWidget(self._qtgui_time_sink_x_2_0_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.menu_grid_layout_6.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_6.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_2 = qtgui.time_sink_f(
            32, #size
            Rs, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_2.set_update_time(0.10)
        self.qtgui_time_sink_x_2.set_y_axis(-1, M)

        self.qtgui_time_sink_x_2.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_2.enable_tags(True)
        self.qtgui_time_sink_x_2.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_2.enable_autoscale(False)
        self.qtgui_time_sink_x_2.enable_grid(False)
        self.qtgui_time_sink_x_2.enable_axis_labels(True)
        self.qtgui_time_sink_x_2.enable_control_panel(False)
        self.qtgui_time_sink_x_2.enable_stem_plot(True)


        labels = ['t4', 'r4', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [3, 3, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, 0, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_2.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_2.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_2.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_2.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_2.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_2.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_2.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_2_win = sip.wrapinstance(self.qtgui_time_sink_x_2.qwidget(), Qt.QWidget)
        self.menu_grid_layout_5.addWidget(self._qtgui_time_sink_x_2_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.menu_grid_layout_5.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_5.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_c(
            32, #size
            Rs, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-1.5, 1.5)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(False)
        self.qtgui_time_sink_x_1.enable_stem_plot(True)


        labels = ['t3 (RE)', 't3 (Im)', 'r3 (Re)', 'r3 (Im)', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [3, 3, 3, 3, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'magenta', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [0, 0, 0, 0, -1,
            -1, -1, -1, -1, -1]


        for i in range(4):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_time_sink_x_1.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_1.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.menu_grid_layout_4.addWidget(self._qtgui_time_sink_x_1_win, 3, 0, 1, 2)
        for r in range(3, 4):
            self.menu_grid_layout_4.setRowStretch(r, 1)
        for c in range(0, 2):
            self.menu_grid_layout_4.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0_0 = qtgui.time_sink_f(
            8*Sps, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0_0.enable_stem_plot(False)


        labels = ['RF', 'r1 (Im)', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [3, 3, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['red', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.menu_grid_layout_7.addWidget(self._qtgui_time_sink_x_0_0_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.menu_grid_layout_7.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_7.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
            16*Sps, #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0_0.enable_tags(True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(False)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)


        labels = ['r0 (Im)', 'r1 (Im)', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [3, 3, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['red', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.qwidget(), Qt.QWidget)
        self.menu_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.menu_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
            16*Sps, #size
            samp_rate, #samp_rate
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-2, 2)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['r0 (Re)', 'r1 (Re)', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [3, 3, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.menu_grid_layout_0.addWidget(self._qtgui_time_sink_x_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.menu_grid_layout_0.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_0.setColumnStretch(c, 1)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title('BER')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.qwidget(), Qt.QWidget)
        self.menu_grid_layout_6.addWidget(self._qtgui_number_sink_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.menu_grid_layout_6.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_6.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-80, 10)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(False)
        self.qtgui_freq_sink_x_0_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)



        labels = ['t3', '', '', '', '',
            '', '', '', '', '']
        widths = [3, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.menu_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.menu_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            2,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-80, 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(0.05)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)



        labels = ['r0', 'r1', '', '', '',
            '', '', '', '', '']
        widths = [3, 3, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.menu_grid_layout_1.addWidget(self._qtgui_freq_sink_x_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.menu_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_1.setColumnStretch(c, 1)
        self.qtgui_eye_sink_x_0 = qtgui.eye_sink_c(
            1024, #size
            samp_rate, #samp_rate
            2, #number of inputs
            None
        )
        self.qtgui_eye_sink_x_0.set_update_time(0.10)
        self.qtgui_eye_sink_x_0.set_samp_per_symbol(Sps)
        self.qtgui_eye_sink_x_0.set_y_axis(-1.8, 1.8)

        self.qtgui_eye_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_eye_sink_x_0.enable_tags(True)
        self.qtgui_eye_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_eye_sink_x_0.enable_autoscale(False)
        self.qtgui_eye_sink_x_0.enable_grid(False)
        self.qtgui_eye_sink_x_0.enable_axis_labels(True)
        self.qtgui_eye_sink_x_0.enable_control_panel(False)


        labels = ['r0 (Re)', 'r0 (Im)', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [4, 4, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'blue', 'blue', 'blue', 'blue',
            'blue', 'blue', 'blue', 'blue', 'blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(4):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
                    self.qtgui_eye_sink_x_0.set_line_label(i, "Eye [Re{{Data {0}}}]".format(round(i/2)))
                else:
                    self.qtgui_eye_sink_x_0.set_line_label(i, "Eye [Im{{Data {0}}}]".format(round((i-1)/2)))
            else:
                self.qtgui_eye_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_eye_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_eye_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_eye_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_eye_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_eye_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_eye_sink_x_0_win = sip.wrapinstance(self.qtgui_eye_sink_x_0.qwidget(), Qt.QWidget)
        self.menu_grid_layout_2.addWidget(self._qtgui_eye_sink_x_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.menu_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_2.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_1 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_1.set_update_time(0.10)
        self.qtgui_const_sink_x_1.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_1.enable_autoscale(False)
        self.qtgui_const_sink_x_1.enable_grid(False)
        self.qtgui_const_sink_x_1.enable_axis_labels(True)


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_1_win = sip.wrapinstance(self.qtgui_const_sink_x_1.qwidget(), Qt.QWidget)
        self.menu_grid_layout_4.addWidget(self._qtgui_const_sink_x_1_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.menu_grid_layout_4.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_4.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_1_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_1_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_1_0.set_y_axis(-1.5, 1.5)
        self.qtgui_const_sink_x_0_1_0.set_x_axis(-1.5, 1.5)
        self.qtgui_const_sink_x_0_1_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_1_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_1_0.enable_grid(False)
        self.qtgui_const_sink_x_0_1_0.enable_axis_labels(True)


        labels = ['p3 (Original)', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_1_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_1_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_1_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_1_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_1_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_1_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_1_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_1_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_1_0.qwidget(), Qt.QWidget)
        self.menu_grid_layout_3.addWidget(self._qtgui_const_sink_x_0_1_0_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.menu_grid_layout_3.setRowStretch(r, 1)
        for c in range(1, 2):
            self.menu_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_1 = qtgui.const_sink_c(
            1024, #size
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_1.set_update_time(0.10)
        self.qtgui_const_sink_x_0_1.set_y_axis(-1.5, 1.5)
        self.qtgui_const_sink_x_0_1.set_x_axis(-1.5, 1.5)
        self.qtgui_const_sink_x_0_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_1.enable_autoscale(False)
        self.qtgui_const_sink_x_0_1.enable_grid(False)
        self.qtgui_const_sink_x_0_1.enable_axis_labels(True)


        labels = ['r3', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_1.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_1.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_1.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_1.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_1.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_1.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_1_win = sip.wrapinstance(self.qtgui_const_sink_x_0_1.qwidget(), Qt.QWidget)
        self.menu_grid_layout_3.addWidget(self._qtgui_const_sink_x_0_1_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.menu_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0_0.enable_grid(False)
        self.qtgui_const_sink_x_0_0.enable_axis_labels(True)


        labels = ['r0 (Vista continua)', 'r1 (Vista continua)', '', '', '',
            '', '', '', '', '']
        widths = [3, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["magenta", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [1, 1, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [-1, -1, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0_0.qwidget(), Qt.QWidget)
        self.menu_grid_layout_3.addWidget(self._qtgui_const_sink_x_0_0_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.menu_grid_layout_3.setRowStretch(r, 1)
        for c in range(1, 2):
            self.menu_grid_layout_3.setColumnStretch(c, 1)
        self.qtgui_const_sink_x_0 = qtgui.const_sink_c(
            1024, #size
            "", #name
            2, #number of inputs
            None # parent
        )
        self.qtgui_const_sink_x_0.set_update_time(0.10)
        self.qtgui_const_sink_x_0.set_y_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_x_axis(-2, 2)
        self.qtgui_const_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, "")
        self.qtgui_const_sink_x_0.enable_autoscale(False)
        self.qtgui_const_sink_x_0.enable_grid(False)
        self.qtgui_const_sink_x_0.enable_axis_labels(True)


        labels = ['r0 (Vista discreta)', 'r1 (Vista discreta)', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "red", "red", "red",
            "red", "red", "red", "red", "red"]
        styles = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        markers = [0, 0, 0, 0, 0,
            0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(2):
            if len(labels[i]) == 0:
                self.qtgui_const_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_const_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_const_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_const_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_const_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_const_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_const_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_const_sink_x_0_win = sip.wrapinstance(self.qtgui_const_sink_x_0.qwidget(), Qt.QWidget)
        self.menu_grid_layout_3.addWidget(self._qtgui_const_sink_x_0_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.menu_grid_layout_3.setRowStretch(r, 1)
        for c in range(0, 1):
            self.menu_grid_layout_3.setColumnStretch(c, 1)
        self.interp_fir_filter_xxx_0_0 = filter.interp_fir_filter_ccf(1, h)
        self.interp_fir_filter_xxx_0_0.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_ccf(Sps, h)
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.fec_ber_bf_0 = fec.ber_bf(False, 100, -7.0)
        self.epy_block_0 = epy_block_0.inversedB()
        self.digital_diff_encoder_bb_0 = digital.diff_encoder_bb(M, digital.DIFF_DIFFERENTIAL)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(M, digital.DIFF_DIFFERENTIAL)
        self.digital_chunks_to_symbols_xx_0 = digital.chunks_to_symbols_bc(constelacion, 1)
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(bps, gr.GR_MSB_FIRST)
        self.blocks_unpack_k_bits_bb_0 = blocks.unpack_k_bits_bb(8)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_packed_to_unpacked_xx_0 = blocks.packed_to_unpacked_bb(bps, gr.GR_MSB_FIRST)
        self.blocks_pack_k_bits_bb_0 = blocks.pack_k_bits_bb(8)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_float*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_1_0_0 = blocks.multiply_const_cc(0.7)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_cc(fading)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_cc(np.exp(1j*Ch_phase))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_cc(1/Sps)
        self.blocks_delay_1_0_0_0 = blocks.delay(gr.sizeof_char*1, retardo_propag*bps)
        self.blocks_delay_1_0_0 = blocks.delay(gr.sizeof_char*1, retardo_propag)
        self.blocks_delay_1_0 = blocks.delay(gr.sizeof_gr_complex*1, retardo_propag)
        self.blocks_delay_1 = blocks.delay(gr.sizeof_gr_complex*1, 0)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, Delay_eye)
        self.blocks_complex_to_float_0_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0 = blocks.complex_to_float(1)
        self.blocks_char_to_float_0_1 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0_0 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self._beta_range = Range(0, 1, 1/100, 1, 200)
        self._beta_win = RangeWidget(self._beta_range, self.set_beta, "beta", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._beta_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.b_upconverter_cf_0 = b_upconverter_cf(
            Fc=Rs*2,
            samp_rate=samp_rate,
        )
        self.b_meter_power_cc_0 = b_meter_power_cc(
            G_prom=0.0001,
        )
        self.b_diezmador_ff_0 = b_diezmador_ff(
            Paso=1000,
        )
        self.b_diez_cc_0 = b_diez_cc(
            M=Timing,
            N=Sps,
        )
        self.b_demod_constelacion_cb_0 = b_demod_constelacion_cb(
            Constelacion=constelacion,
        )
        self.b_FLL_tunner2_0 = b_FLL_tunner2(
            Constellation=constelacion,
        )
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, ch_freq, 1, 0, 0)
        self.analog_random_source_x_0 = blocks.vector_source_b(list(map(int, numpy.random.randint(0, 2, 1000))), True)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, math.sqrt(Pn), 0)
        self.analog_agc3_xx_0 = analog.agc3_cc(1e-3, 1e-4, 1.0, 1.0, 1)
        self.analog_agc3_xx_0.set_max_gain(65536)
        self._Gain_USRP_Tx_dB_range = Range(0., 130, 1, 30., 200)
        self._Gain_USRP_Tx_dB_win = RangeWidget(self._Gain_USRP_Tx_dB_range, self.set_Gain_USRP_Tx_dB, "Gain_USRP_Tx (dB)", "counter", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._Gain_USRP_Tx_dB_win, 3, 1, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._Gain_USRP_Rx_dB_range = Range(0., 130, 1, 20, 200)
        self._Gain_USRP_Rx_dB_win = RangeWidget(self._Gain_USRP_Rx_dB_range, self.set_Gain_USRP_Rx_dB, "Gain_USRP_Rx (dB)", "counter", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._Gain_USRP_Rx_dB_win, 4, 1, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._BW_filtro_range = Range(0, Fmax, Fmax/100, Fmax, 200)
        self._BW_filtro_win = RangeWidget(self._BW_filtro_range, self.set_BW_filtro, "'BW_filtro'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._BW_filtro_win, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc3_xx_0, 0), (self.b_FLL_tunner2_0, 0))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_delay_1_0_0_0, 0))
        self.connect((self.analog_random_source_x_0, 0), (self.blocks_pack_k_bits_bb_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.b_FLL_tunner2_0, 0), (self.b_demod_constelacion_cb_0, 0))
        self.connect((self.b_FLL_tunner2_0, 0), (self.qtgui_const_sink_x_0_1, 0))
        self.connect((self.b_FLL_tunner2_0, 0), (self.qtgui_const_sink_x_1, 0))
        self.connect((self.b_FLL_tunner2_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.b_FLL_tunner2_0, 0), (self.qtgui_time_sink_x_1, 1))
        self.connect((self.b_demod_constelacion_cb_0, 0), (self.digital_diff_decoder_bb_0, 0))
        self.connect((self.b_diez_cc_0, 0), (self.analog_agc3_xx_0, 0))
        self.connect((self.b_diezmador_ff_0, 0), (self.qtgui_time_sink_x_3, 0))
        self.connect((self.b_meter_power_cc_0, 1), (self.b_diezmador_ff_0, 0))
        self.connect((self.b_meter_power_cc_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.b_meter_power_cc_0, 2), (self.blocks_null_sink_0, 1))
        self.connect((self.b_upconverter_cf_0, 0), (self.qtgui_time_sink_x_0_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_delay_1, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.qtgui_time_sink_x_2, 0))
        self.connect((self.blocks_char_to_float_0_0, 0), (self.qtgui_time_sink_x_2, 1))
        self.connect((self.blocks_char_to_float_0_0_0, 0), (self.qtgui_time_sink_x_2_0, 1))
        self.connect((self.blocks_char_to_float_0_1, 0), (self.qtgui_time_sink_x_2_0, 0))
        self.connect((self.blocks_complex_to_float_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.blocks_complex_to_float_0, 1), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.blocks_complex_to_float_0_0, 0), (self.qtgui_time_sink_x_0, 1))
        self.connect((self.blocks_complex_to_float_0_0, 1), (self.qtgui_time_sink_x_0_0, 1))
        self.connect((self.blocks_delay_0, 0), (self.qtgui_eye_sink_x_0, 0))
        self.connect((self.blocks_delay_0, 1), (self.qtgui_eye_sink_x_0, 1))
        self.connect((self.blocks_delay_1, 0), (self.b_meter_power_cc_0, 0))
        self.connect((self.blocks_delay_1, 0), (self.b_upconverter_cf_0, 0))
        self.connect((self.blocks_delay_1, 0), (self.blocks_complex_to_float_0, 0))
        self.connect((self.blocks_delay_1, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_delay_1, 0), (self.interp_fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_delay_1, 0), (self.qtgui_const_sink_x_0, 0))
        self.connect((self.blocks_delay_1, 0), (self.qtgui_const_sink_x_0_0, 0))
        self.connect((self.blocks_delay_1, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.blocks_delay_1_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.blocks_delay_1_0_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.blocks_delay_1_0_0_0, 0), (self.blocks_char_to_float_0_1, 0))
        self.connect((self.blocks_delay_1_0_0_0, 0), (self.fec_ber_bf_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.b_diez_cc_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_complex_to_float_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_delay_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_const_sink_x_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_const_sink_x_0_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_freq_sink_x_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_pack_k_bits_bb_0, 0), (self.blocks_packed_to_unpacked_xx_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.blocks_delay_1_0_0, 0))
        self.connect((self.blocks_packed_to_unpacked_xx_0, 0), (self.digital_diff_encoder_bb_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.blocks_char_to_float_0_0_0, 0))
        self.connect((self.blocks_unpack_k_bits_bb_0, 0), (self.fec_ber_bf_0, 1))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.blocks_unpack_k_bits_bb_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_delay_1_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.blocks_multiply_const_vxx_1_0_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0, 0), (self.qtgui_const_sink_x_0_1_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_char_to_float_0_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))
        self.connect((self.digital_diff_encoder_bb_0, 0), (self.digital_chunks_to_symbols_xx_0, 0))
        self.connect((self.epy_block_0, 0), (self.qtgui_number_sink_0, 0))
        self.connect((self.fec_ber_bf_0, 0), (self.epy_block_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.interp_fir_filter_xxx_0_0, 0), (self.blocks_multiply_const_vxx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "waveforming_practice")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_constelacion(self):
        return self.constelacion

    def set_constelacion(self, constelacion):
        self.constelacion = constelacion
        self.set_M(len(self.constelacion ))
        self.b_FLL_tunner2_0.set_Constellation(self.constelacion)
        self.b_demod_constelacion_cb_0.set_Constelacion(self.constelacion)
        self.digital_chunks_to_symbols_xx_0.set_symbol_table(self.constelacion)

    def get_Sps(self):
        return self.Sps

    def set_Sps(self, Sps):
        self.Sps = Sps
        self.set_h([1]*self.Sps)
        self.set_ntaps(16*self.Sps)
        self.set_samp_rate(self.Rs*self.Sps)
        self.b_diez_cc_0.set_N(self.Sps)
        self.blocks_multiply_const_vxx_0.set_k(1/self.Sps)
        self.qtgui_eye_sink_x_0.set_samp_per_symbol(self.Sps)

    def get_Rs(self):
        return self.Rs

    def set_Rs(self, Rs):
        self.Rs = Rs
        self.set_Rb(self.Rs*self.bps)
        self.set_samp_rate(self.Rs*self.Sps)
        self.b_upconverter_cf_0.set_Fc(self.Rs*2)
        self.qtgui_time_sink_x_1.set_samp_rate(self.Rs)
        self.qtgui_time_sink_x_2.set_samp_rate(self.Rs)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_Fmax(self.samp_rate/2)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.b_upconverter_cf_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)
        self.qtgui_eye_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(0, self.samp_rate)
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_3.set_samp_rate(self.samp_rate)

    def get_M(self):
        return self.M

    def set_M(self, M):
        self.M = M
        self.set_bps(int(math.log(self.M,2)))
        self.qtgui_time_sink_x_2.set_y_axis(-1, self.M)

    def get_bps(self):
        return self.bps

    def set_bps(self, bps):
        self.bps = bps
        self.set_Rb(self.Rs*self.bps)
        self.blocks_delay_1_0_0_0.set_dly(self.retardo_propag*self.bps)

    def get_Fmax(self):
        return self.Fmax

    def set_Fmax(self, Fmax):
        self.Fmax = Fmax
        self.set_BW_filtro(self.Fmax)

    def get_retardo_propag(self):
        return self.retardo_propag

    def set_retardo_propag(self, retardo_propag):
        self.retardo_propag = retardo_propag
        self.blocks_delay_1_0.set_dly(self.retardo_propag)
        self.blocks_delay_1_0_0.set_dly(self.retardo_propag)
        self.blocks_delay_1_0_0_0.set_dly(self.retardo_propag*self.bps)

    def get_ntaps(self):
        return self.ntaps

    def set_ntaps(self, ntaps):
        self.ntaps = ntaps

    def get_h(self):
        return self.h

    def set_h(self, h):
        self.h = h
        self.interp_fir_filter_xxx_0.set_taps(self.h)
        self.interp_fir_filter_xxx_0_0.set_taps(self.h)

    def get_fading(self):
        return self.fading

    def set_fading(self, fading):
        self.fading = fading
        self.blocks_multiply_const_vxx_1_0.set_k(self.fading)

    def get_ch_freq(self):
        return self.ch_freq

    def set_ch_freq(self, ch_freq):
        self.ch_freq = ch_freq
        self.analog_sig_source_x_0.set_frequency(self.ch_freq)

    def get_beta(self):
        return self.beta

    def set_beta(self, beta):
        self.beta = beta

    def get_Timing(self):
        return self.Timing

    def set_Timing(self, Timing):
        self.Timing = Timing
        self.b_diez_cc_0.set_M(self.Timing)

    def get_Rb(self):
        return self.Rb

    def set_Rb(self, Rb):
        self.Rb = Rb
        self.qtgui_time_sink_x_2_0.set_samp_rate(self.Rb)

    def get_Pn(self):
        return self.Pn

    def set_Pn(self, Pn):
        self.Pn = Pn
        self.analog_noise_source_x_0.set_amplitude(math.sqrt(self.Pn))

    def get_Gain_USRP_Tx_dB(self):
        return self.Gain_USRP_Tx_dB

    def set_Gain_USRP_Tx_dB(self, Gain_USRP_Tx_dB):
        self.Gain_USRP_Tx_dB = Gain_USRP_Tx_dB

    def get_Gain_USRP_Rx_dB(self):
        return self.Gain_USRP_Rx_dB

    def set_Gain_USRP_Rx_dB(self, Gain_USRP_Rx_dB):
        self.Gain_USRP_Rx_dB = Gain_USRP_Rx_dB

    def get_Delay_eye(self):
        return self.Delay_eye

    def set_Delay_eye(self, Delay_eye):
        self.Delay_eye = Delay_eye
        self.blocks_delay_0.set_dly(self.Delay_eye)

    def get_Ch_phase(self):
        return self.Ch_phase

    def set_Ch_phase(self, Ch_phase):
        self.Ch_phase = Ch_phase
        self.blocks_multiply_const_vxx_1.set_k(np.exp(1j*self.Ch_phase))

    def get_BW_filtro(self):
        return self.BW_filtro

    def set_BW_filtro(self, BW_filtro):
        self.BW_filtro = BW_filtro




def main(top_block_cls=waveforming_practice, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
