# **************************************************************************
# *
# * Authors:     Pablo Conesa (pconesa@cnb.csic.es) [1]
# *              Peter Horvath (phorvath@cnb.csic.es) [1]
# *
# * [1] I2PC center
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

from .test_protocol_janni import *
from .test_protocol_cryolo import *


DataSet(name='negative_stain',
        folder='negative_stain',
        files={
            'allMics': '*.tif',
            'mic1': '8b001.tif',
            'mic2': '20180612_SOS1_dil2_SS2_009.tif',
        })

DataSet(name='tomo-em', folder='tomo-em',
        files={
               'tomo1': 'overview_wbp.em',
               'tomo2': 'overview_wbp2.em',
               'tomo3': 'tomo_8_mn.mrc',
               'subtomo': 'basename.hdf',
               'eman_coordinates': 'coordinates3Deman2',
               'etomo': 'tutorialData',
               'empiar': 'EMPIAR-10164',
               'tsMParentFolder': 'ts_tsM_and_mdocs',
               'tsM10Dir': 'ts_tsM_and_mdocs/Tomo_10',
               'tsM31Dir': 'ts_tsM_and_mdocs/Tomo_31',
               'empiarMdocDirOk': 'ts_tsM_and_mdocs/mdocs/realFromEmpiar/complete',
               'empiarMdocDirNoOk': 'ts_tsM_and_mdocs/mdocs/realFromEmpiar/incomplete',
               'realFileNoVoltage1': 'tomo4_delay.st.mdoc',
               'realFileNoVoltage2': 'TS_54.mrc.mdoc',
               'simErrorMdocDir': 'ts_tsM_and_mdocs/mdocs/editedForErrorSimulation',
               'noMaginficationMdoc': 'NoMagnification.mdoc',
               'noSamplingRateMdoc': 'NoPixelSpacing.mdoc',
               'noVoltagenoSRateMdoc': 'NoVoltage_NoPixelSpacing.mdoc',
               'someMissingAnglesMdoc': 'SomeTiltAnglesMissing_1_7_48.mdoc',
               'noDoseMdoc': 'noDose.mdoc'
        })
