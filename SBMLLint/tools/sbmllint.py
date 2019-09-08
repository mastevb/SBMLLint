"""Checks for static errors in a model."""

from SBMLLint.common import config
from SBMLLint.common import constants as cn
from SBMLLint.common.simple_sbml import SimpleSBML
from SBMLLint.common import util
from SBMLLint.games.games_pp import GAMES_PP
from SBMLLint.games.games_report import GAMESReport
from SBMLLint.structured_names.moiety_comparator import MoietyComparator

import argparse
import os
import sys
import tesbml

TYPE_I = "type1"
TYPE_II = "type2"
TYPE_III = "type3"
CANCELING = "canceling"
ECHELON = "echelon"


def lint(model_reference, file_out=sys.stdout,
    mass_balance_check="structured_names",
    config_path=None,
    is_report=True,
    implicit_games=False):
  """
  Reports on errors found in a model
  :param str model_reference: 
      libsbml_model, file, antimony string, xml string
  :param TextIOWrapper file_out:
  :param str mass_balance_check: how check for mass balance
  :param str config_path: path to configuration file
  :param bool is_report: print result
  :return MoietyComparatorResult/bull/None:
  """
  config.setConfiguration(path=config_path)
  config_dict = config.getConfiguration()
  if util.isSBMLModel(model_reference):
    model = model_reference
  else:
    xml = util.getXML(model_reference)
    reader = tesbml.SBMLReader()
    document = reader.readSBMLFromString(xml)
    util.checkSBMLDocument(document)
    model = document.getModel()
  simple = SimpleSBML()
  simple.initialize(model)
  if mass_balance_check == "structured_names":
    result = MoietyComparator.analyzeReactions(simple,
        implicits=config_dict['implicits'])
    if is_report:
      for line in result.report.split('\n'):
          file_out.write("%s\n" % line)
    return result
  elif mass_balance_check == "games":
    if implicit_games:
      for implicit in config_dict['implicits']:
        simple = removeImplicit(simple, implicit)
      # print("implicit - results")
      # for r in simple.reactions:
      #   print(r.makeIdentifier(is_include_kinetics=False))
    m = GAMES_PP(simple)
    games_result = m.analyze(simple.reactions)
    if games_result and is_report:
      gr = GAMESReport(m)
      errortype_dic = {TYPE_I: gr.reportTypeOneError,
                       TYPE_II: gr.reportTypeTwoError,
                       TYPE_III: gr.reportTypeThreeError,
                       CANCELING: gr.reportCancelingError,
                       ECHELON: gr.reportEchelonError
                      }
      for errors in m.error_summary:
        for category in errortype_dic.keys():
          if errors.type == category:
            func = errortype_dic[category]            
            report, _ = func(errors.errors, explain_details=True)
            print(report)
    return games_result
  else:
    print ("Specified method doesn't exist")
    return None

def removeImplicit(simple, implicit):
  """
  Remove an implicit molecule
  from all reactions in a simpleSBML model.
  :param SimpleSBML simple:
  :param str implicit:
  :return SimpleSBML:
  """
  modified_reactions = []
  for r in simple.reactions:
    modified = False
    reactant_names = [reactant.molecule.name for reactant in r.reactants]
    product_names = [product.molecule.name for product in r.products]
    if implicit in reactant_names:
      r.reactants = [ms for ms in r.reactants if ms.molecule.name != implicit]
      modified = True
    if implicit in product_names:
      r.products = [ms for ms in r.products if ms.molecule.name != implicit]
      modified = True
    r.identifier = r.makeIdentifier()
    r.category = r.getCategory()
    if modified:
      modified_reactions.append(r)
  return simple


def main():
  parser = argparse.ArgumentParser(description='SBML XML file.')
  parser.add_argument('filename', type=str, help='SBML file')
  args = parser.parse_args()
  lint(args.filename)


if __name__ == '__main__':
  main()
