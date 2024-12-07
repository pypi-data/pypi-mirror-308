#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generates different versions of a LaTeX test exam and evaluates the answers
provided by the students.
"""

###########################################################################
#  latext_test.py                                                         #
#  ---------------------------------------------------------------------  #
#    copyright            : (C) 2024 by Sergio Barrachina Mir             #
#    email                : barrachi@uji.es                               #
###########################################################################

###########################################################################
#                                                                         #
#  This program is free software; you can redistribute it and/or modify   #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation; either version 2 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  This program is distributed in the hope that it will be useful, but    #
#  WITHOUT ANY WARRANTY; without even the implied warranty of             #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU      #
#  General Public License for more details.                               #
#                                                                         #
###########################################################################

import sys

import TexSoup
import argparse
import json
import os
import pandas as pd
import pathlib
import random
import shutil
from dataclasses import dataclass
from rich import print as rich_print
from rich.panel import Panel
from tqdm import tqdm


###########################################################################
# Global constants
###########################################################################
SCRIPT_PATH = pathlib.Path(__file__).parent.absolute()
SCRIPT_NAME = os.path.basename(pathlib.Path(__file__))
ABCDE = 'ABCDEFGHIJ'
abcde = 'abcdefghij'
DNI = "DNI"
NAME = "Nom alumne"
TYPE = "Tipo"
ANSWERS = 'Respuestas'
CORRECT_ANSWERS = 'Correctas'
FAILED_ANSWERS = 'Falladas'
PENALTY = 'Penalización'
MARK_WO_PENALTY = 'NotaSinPenalización'
MARK = 'Nota'
ANSWERED_CORRECTS = 'Contestadas:Correctas'


###########################################################################
# MISCELLANEOUS FUNCTIONS                                                 #
###########################################################################


def log(text):
    """Logs a message to stderr."""
    sys.stderr.write(f">>> {text}\n")


def error(text):
    """Reports an error message and exit."""
    sys.stderr.write(f"{SCRIPT_NAME}:error: {text}\n")
    sys.exit(-1)


###########################################################################
# APPLICATION SPECIFIC FUNCTIONS                                          #
###########################################################################

@dataclass
class ExamParts:
    soup: TexSoup.data.TexNode
    tex_questions: [TexSoup.data.TexNode]
    tex_questions_enumerates: [TexSoup.data.TexNode]
    tex_answers: [[TexSoup.data.TexNode]]
    correct_answers: [[int]]
    do_shuffle_answers: [bool]
    do_keep_last_answer: [bool]
    do_cancel_question: [bool]


def detach(item_or_items):
    """
    Detaches the given TexSoup item or items and returns a
    parentless copy of them.
    """
    if type(item_or_items) is list:
        # Delete objects from the tree
        [x.delete() for x in item_or_items]
        # Return a copy (without a parent) of these objects
        return [x.copy() for x in item_or_items]
    else:
        # Delete object from the tree
        item_or_items.delete()
        # Return a copy (without a parent) of the object
        return item_or_items.copy()


def disassemble(tex_file):
    """Disassembles a LaTeX test exam file"""
    soup = TexSoup.TexSoup(tex_file)
    # Get enumerate
    enum = soup.document.enumerate
    # Get questions in enumerate
    tex_questions = detach([x for x in enum.children if x.name == 'item'])
    # Get last enumerate of each question and associated question data
    tex_questions_enumerates = []
    correct_answers = []
    do_shuffle_answers = []
    do_keep_last_answer = []
    do_cancel_question = []
    for question in tex_questions:
        last_enumerate = [x for x in question.children if x.name == 'enumerate'][-1]
        tex_questions_enumerates.append(detach(last_enumerate))
        correct_answers_tex_nodes = detach(last_enumerate.find_all('respuesta'))
        correct_answers.append([abcde.index(x.string.lower()) for x in correct_answers_tex_nodes])
        correct_answers[-1].sort()
        shuffle_answers_tex_nodes = detach(last_enumerate.find_all('nobarajar'))
        do_shuffle_answers.append(len(shuffle_answers_tex_nodes) == 0)
        keep_last_answer_tex_nodes = detach(last_enumerate.find_all('ninguna'))
        do_keep_last_answer.append(len(keep_last_answer_tex_nodes) > 0)
        cancel_question_tex_nodes = detach(last_enumerate.find_all('anular'))
        do_cancel_question.append(len(cancel_question_tex_nodes) > 0)
    tex_answers = []
    for q_enumerate in tex_questions_enumerates:
        tex_answers.append(detach([x for x in q_enumerate.children if x.name == 'item']))
    parts = ExamParts(soup,
                      tex_questions,
                      tex_questions_enumerates,
                      tex_answers,
                      correct_answers,
                      do_shuffle_answers,
                      do_keep_last_answer,
                      do_cancel_question)
    return parts


def info(args):
    rich_print(Panel.fit(f"[blue]Información extraida del fichero [green]'{args.texfile.name}'"))
    rows = []
    for i in range(len(args.parts.tex_questions)):
        data = {"Pregunta": i + 1,
                "Correctas": [ABCDE[x] for x in args.parts.correct_answers[i]],
                "Respuestas": len(args.parts.tex_answers[i]),
                "Barajar": "*   " if args.parts.do_shuffle_answers[i] else "",
                "Dejar últ.": "*   " if args.parts.do_keep_last_answer[i] else "",
                "Anular": "XXX" if args.parts.do_cancel_question[i] else "",
                }
        rows.append(data)
    df = pd.DataFrame(rows).set_index("Pregunta")
    print(df)
    print()


def shuffle_of(n):
    """Returns a list of shuffled indexes of side n"""
    indexes = list(range(n))
    shuffled = []
    while indexes:
        shuffled.append(indexes.pop(random.randrange(0, len(indexes))))
    return shuffled


def shuffle(args):
    # Check if the output dir already exists
    if os.path.exists(args.output_dir):
        error(f"Output dir '{args.output_dir}' already exists. "
              f"The shuffle command should only be called once.")
    # Create the output dir
    print(f"Creating the directory '{args.output_dir}'")
    os.mkdir(args.output_dir)
    # Copy includes and Plots directories
    for directory in ["includes", "Plots"]:
        origin = os.path.join(args.input_dir, directory)
        print(f"Copying '{directory}' to '{args.output_dir}'")
        if os.path.isdir(origin):
            shutil.copytree(origin, os.path.join(args.output_dir, directory))
    # Make a copy of the original exam
    print(f"Making a copy of '{args.texfile.name}' in '{args.output_dir}'...")
    tex_file_copy_name = os.path.join(args.output_dir, "copy_of_" + args.texfile.name)
    shutil.copy(args.texfile.name, tex_file_copy_name)
    # Shuffle the questions and answers for each exam version
    print(f"Shuffling the exam {args.n} times...")
    exams = []
    for i in range(args.n):
        questions_shuffled = shuffle_of(len(args.parts.tex_questions))
        answers_shuffled = []
        for q in questions_shuffled:
            n_answers = len(args.parts.tex_answers[q])
            if args.parts.do_shuffle_answers[q]:
                if args.parts.do_keep_last_answer:
                    qa_shuffled = shuffle_of(n_answers - 1) + [n_answers - 1]
                else:
                    qa_shuffled = shuffle_of(n_answers)
            else:
                qa_shuffled = list(range(n_answers))
            answers_shuffled.append(qa_shuffled)
        exams.append(list(zip(questions_shuffled, answers_shuffled)))
    # Write exams to a json file
    with open(args.json_file_name, 'w') as output_file:
        json.dump(exams, output_file)
    # Read exams from the json file
    with open(args.json_file_name, 'r') as input_file:
        exams = json.load(input_file)
    # Generate shuffled versions
    for e in tqdm(range(args.n)):
        code = f'{e:03}'
        output_file_name = os.path.join(args.output_dir, f"{code}.tex")
        # print(f"Generating {output_file_name}...")
        with open(tex_file_copy_name, 'r') as tex_file_copy:
            # @warning: This is required as TexSoup copy() does linked copies, not real copies
            args.parts = disassemble(tex_file_copy)
        tex = args.parts.soup
        renew_clave = TexSoup.TexSoup(f"\n\n\\renewcommand{{\\clave}}{{{code}}}")
        tex.document.insert(0, renew_clave)
        for q, answers_shuffled in exams[e]:
            question = args.parts.tex_questions[q]  # .copy()
            q_enumerate = args.parts.tex_questions_enumerates[q]  # .copy()
            for a in answers_shuffled:
                q_enumerate.append(args.parts.tex_answers[q][a])  # .copy())
            question.append(q_enumerate)
            question.append("\n\n")
            tex.document.enumerate.append(question)
        # Write the new version
        with open(output_file_name, 'w') as output_file:
            previous_line_was_blank = False
            for tex_node in tex.all:
                for line in str(tex_node).split('\n'):
                    if line.strip() == '' and previous_line_was_blank:
                        continue
                    output_file.write(f"{line.rstrip()}\n")
                    previous_line_was_blank = (line.strip() == '')
    # Done!
    print("Done!")


def do_correct_answers(args, exams, answers_df):
    def correct_answers_of(row):
        if pd.isnull(row[TYPE]) and pd.isnull(row[ANSWERS]):
            return {}  # empty dict
        if pd.isnull(row[TYPE]) or pd.isnull(row[ANSWERS]):
            error(f"The next record has only one of 'Tipo' and 'Respuestas':\n{row}")
        nexams = len(exams)
        if row[TYPE] < 0 or row[TYPE] >= nexams:
            error(f"The 'Tipo' in the next record should be between 0 and {nexams - 1}:\n{row}")
        nquestions = len(exams[0])
        if len(row[ANSWERS]) != nquestions:
            error(f"The number of answers in the next record is not {nquestions}:\n{row}")
        corrects = 0
        failed = 0
        penalty = 0
        answered_vs_corrects = []
        for (q, qa), sa in zip(exams[row[TYPE]], row[ANSWERS].upper()):
            # If the question is canceled, continue
            if args.parts.do_cancel_question[q]:
                answered_vs_corrects.append(':')
                continue
            # Correct answers
            correct_answers = args.parts.correct_answers[q]
            correct_answers_txt = ''.join([ABCDE[x] for x in correct_answers])
            # If student answer is not a letter, continue
            if sa not in ABCDE:
                answered_vs_corrects.append(f":{correct_answers_txt}")
                continue
            # Correct the answer
            student_answer = qa[ABCDE.index(sa)]
            if student_answer in correct_answers:
                corrects += 1
            else:
                failed += 1
                penalty += 1 / (len(qa) - len(correct_answers))
            answered_vs_corrects.append(f'{sa}:{correct_answers_txt}')
        n_valid = len([x for x in args.parts.do_cancel_question if x is False])
        mark_wo_penalty = (10 * corrects) / n_valid
        mark = max((10 * (corrects - penalty)) / n_valid, 0)
        return {CORRECT_ANSWERS: corrects,
                FAILED_ANSWERS: failed,
                PENALTY: penalty,
                MARK_WO_PENALTY: mark_wo_penalty,
                MARK: mark,
                ANSWERED_CORRECTS: answered_vs_corrects,
                }

    columns = [CORRECT_ANSWERS, FAILED_ANSWERS, PENALTY, MARK_WO_PENALTY, MARK, ANSWERED_CORRECTS]
    answers_df[columns] = answers_df.apply(correct_answers_of, axis=1, result_type='expand')
    for column in [CORRECT_ANSWERS, 'Falladas']:
        answers_df[column] = answers_df[column].astype('Int64')
    print(answers_df.head())
    print("...")
    output_csvfile_name = args.csvfile.name.replace('.csv', '_corregido.csv')
    rich_print(f"[blue]Guardando los resultados en [green]'{output_csvfile_name}'[blue]...")
    answers_df.to_csv(output_csvfile_name, sep=';', index=False)


def do_generate_tex_answers(args, answers_df):
    def renew_command(key, value):
        return rf"\renewcommand{{\{key}}}{{{value}}}"

    labels_lines = [r"\newcommand{\asignatura}{}"
                    r"\newcommand{\convocatoria}{}",
                    r"\input{includes/parametros.tex}",
                    r"\begin{document}",
                    r""]
    la_keys = ['uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez', 'once',
               'doce', 'trece', 'catorce', 'quince', 'dseis', 'dsiete', 'docho', 'dnueve', 'veinte']
    lca_keys = ['sol' + x for x in la_keys]

    def renew_answer_command(question_number, answer, correct_answers):
        if answer in correct_answers:
            return renew_command(la_keys[question_number], rf"{answer}\bien") + "\t" + \
                renew_command(lca_keys[question_number], rf" ")
        else:
            return renew_command(la_keys[question_number], rf"{answer}\mal") + "\t" + \
                renew_command(lca_keys[question_number], rf"{correct_answers}")

    def renew_not_answered_command(question_number, correct_answers):
        return renew_command(la_keys[question_number], rf" ") + "\t" + \
            renew_command(lca_keys[question_number], rf"{correct_answers}")

    def get_lines_of(row):
        if pd.isnull(row[TYPE]):
            return None
        answer_lines = []
        last_name, first_name = row[NAME].split(',')
        answer_lines.append(renew_command('apellidos', last_name))
        answer_lines.append(renew_command('nombre', first_name))
        answer_lines.append(renew_command('dni', row[DNI]))
        answer_lines.append(renew_command('clave', row[TYPE]))

        n_valid = len([x for x in args.parts.do_cancel_question if x is False])
        answer_lines.append(renew_command('nbien', row[CORRECT_ANSWERS]))
        answer_lines.append(renew_command('nmal', row[FAILED_ANSWERS]))
        answer_lines.append(renew_command('nnc', n_valid - row[CORRECT_ANSWERS] - row[FAILED_ANSWERS]))
        answer_lines.append(renew_command('nota', row[MARK]))

        for q, a_c in enumerate(row[ANSWERED_CORRECTS]):
            student_answer, correct_answers = a_c.split(':')
            answer_lines.append(renew_answer_command(q, student_answer, correct_answers))
        return answer_lines

    lines_df = answers_df.apply(get_lines_of, axis=1, result_type='expand')
    rich_print(lines_df)

    def write_answers_of(row):
        for item in row:
            labels_file.write(str(item) + '\n')
        labels_file.write(r"\input{includes/plantilla_tickets.tex}" + '\n')

    rich_print("[blue]Generando el fichero [green]'etiquetas.tex'[blue]...")
    with open(os.path.join(args.output_dir, "etiquetas.tex"), "w") as labels_file:
        labels_file.write(r"\newcommand{\etiqueta}{true}" + '\n')
        labels_file.write(r"\input{includes/parametros.tex}" + '\n')
        labels_file.write(r"\begin{document}" + '\n')
        lines_df.apply(write_answers_of, axis=1)
        labels_file.write(r"\end{document}" + '\n')


def correct(args):
    rich_print(Panel.fit(f"[blue]Corrigiendo las respuestas de [green]'{args.csvfile.name}'"))
    # Read exams from the json file
    with open(args.json_file_name, 'r') as input_file:
        exams = json.load(input_file)
    # Read answers from the csv file
    answers_df = pd.read_csv(args.csvfile, sep=";", dtype={'Tipo': 'Int64', 'Respuestas': 'str'})
    answers_df = answers_df.loc[(pd.isna(answers_df[TYPE]) == False) & (pd.isna(answers_df[ANSWERS]) == False)]
    print(answers_df.head())
    print("...")
    # Correct answers
    do_correct_answers(args, exams, answers_df)
    # Generate tex files with the answers
    do_generate_tex_answers(args, answers_df)


def parse_args():
    """Parses command line args"""
    parser = argparse.ArgumentParser(  # usage="%(prog)s [OPTION]... ACTION TEXFILE",
        description="Generates different versions of a LaTeX test "
                    "exam and corrects the answers provided by the students.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    texfile_help = "the LaTex exam"

    info_parser = subparsers.add_parser('info',
                                        help="provides info about the given latex exam")
    info_parser.add_argument('texfile', type=argparse.FileType('r'),
                             help=texfile_help)
    info_parser.set_defaults(func=info)

    shuffle_parser = subparsers.add_parser('shuffle',
                                           help="generates N shuffled versions of the given latex exam")
    shuffle_parser.add_argument('n', type=int,
                                help="the number of shuffled versions to be generated")
    shuffle_parser.add_argument('texfile', type=argparse.FileType('r'),
                                help=texfile_help)
    shuffle_parser.set_defaults(func=shuffle)

    correct_parser = subparsers.add_parser('correct',
                                           help="corrects the answers given for the previously shuffled exams")
    correct_parser.add_argument('csvfile', type=argparse.FileType('r'),
                                help="csv file with the students answers")
    correct_parser.add_argument('texfile', type=argparse.FileType('r'),
                                help=texfile_help)
    correct_parser.set_defaults(func=correct)

    # Parse command line args
    args = parser.parse_args()

    # Check files
    if getattr(args, 'csvfile', None) and args.csvfile.name[-4:].lower() != '.csv':
        correct_parser.print_help()
        error(f"Expecting a CSV file where '{args.csvfile.name}' was provided")
    if args.texfile.name[-4:].lower() != '.tex':
        errmsg = f"Expecting a TEX file where '{args.texfile.name}' was provided"
        if args.command == "info":
            info_parser.print_help()
            error(errmsg)
        elif args.command == "shuffle":
            shuffle_parser.print_help()
            error(errmsg)
        else:
            correct_parser.print_help()
            error(errmsg)

    # Add input_dir, output_dir, and json_file_name to args
    args.input_dir = os.path.abspath(os.path.dirname(args.texfile.name))
    args.output_dir = os.path.abspath(args.texfile.name)[:-4] + "_shuffled"
    args.json_file_name = os.path.join(args.output_dir, "exams.json")

    # Add the latex file parts to args
    args.parts = disassemble(args.texfile)

    # Call the appropriate command function
    args.func(args)


def main():
    """Do the work (main function, called when not imported)."""
    parse_args()


if __name__ == "__main__":
    main()
