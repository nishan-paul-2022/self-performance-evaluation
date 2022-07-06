from django.shortcuts import render
from collections import defaultdict
from main import models
import math
import json

v1stStart = '2004'
v2ndLast = '2021'
v3rdCurrent = '2022'

weight_year_a = ['book', 'routine_2am_7am', 'writing', 'study_time', 'response_teacher', 'response_friend']
weight_year_b = ['pro_contest', 'pro_solving', 'soft_developing', 'research', 'algorithm', 'software', 'online_course']
weight_year_c = ['academic']
node_undergraduate = ['l1t1', 'l1t2', 'l2t1', 'l2t2', 'l3t1', 'l3t2', 'l4t1', 'l4t2']
didnt = ['F', '+', '-']

gpa_system = {
    4.00: [80, 'A+'], 3.75: [75, 'A'], 3.50: [70, 'A-'],
    3.25: [65, 'B+'], 3.00: [60, 'B'], 2.75: [55, 'B-'],
    2.50: [50, 'C+'], 2.25: [45, 'C'],
    2.00: [40, 'D']
}

mission = 10000
target_hours_daily = 14
week = 7
statistics_years_details = dict()

func_undergraduate = lambda row, odd, options: row.grade not in didnt
func_result = lambda row, odd, options: row.grade == '-'
func_exam = lambda row, odd, options: row.grade == '+'
func_short = lambda row, odd, options: row.grade == 'F'
func_level = lambda row, odd, options: row.level == options and row.grade not in didnt
func_dept = lambda row, odd, options: 'CSE' in row.code and row.grade not in didnt
func_nondept = lambda row, odd, options: 'CSE' not in row.code and row.grade not in didnt
func_theo = lambda row, odd, options: odd == True and row.grade not in didnt
func_sess = lambda row, odd, options: odd == False and row.grade not in didnt
func_theo_dept = lambda row, odd, options: odd == True and 'CSE' in row.code and row.grade not in didnt
func_sess_dept = lambda row, odd, options: odd == False and 'CSE' in row.code and row.grade not in didnt
func_theo_nondept = lambda row, odd, options: odd == True and 'CSE' not in row.code and row.grade not in didnt
func_sess_nondept = lambda row, odd, options: odd == False and 'CSE' not in row.code and row.grade not in didnt
func_sess_only = lambda row, odd, options: 'ONLY' in row.name and row.grade not in didnt

undergraduate_functions = [
    func_undergraduate, func_result, func_exam, func_short,
    func_level, func_level, func_level, func_level, func_level, func_level, func_level, func_level,
    func_dept, func_nondept, func_theo, func_sess, func_theo_dept, func_sess_dept, func_theo_nondept, func_sess_nondept,
    func_sess_only
]

undergraduate_options = [
    "undergraduate", "result", "exam", "short",
    "l1t1", "l1t2", "l2t1", "l2t2", "l3t1", "l3t2", "l4t1", "l4t2",
    "dept", "nondept", "theo", "sess", "theo_dept", "sess_dept", "theo_nondept", "sess_nondept", "sess_only"
]


def get_details_from_cgpa(value):
    global gpa_system
    for i in gpa_system:
        if value >= i:
            return gpa_system[i][0], gpa_system[i][1]
    return 0, 'X'


def show_undergraduate_details():
    global undergraduate_options, undergraduate_functions
    data_undergraduate = models.Undergraduate.objects.all()
    data_undergraduate = sorted(data_undergraduate, key=lambda i: i.id)
    undergraduate_details = defaultdict(lambda: list())

    for row in data_undergraduate:
        odd = 'SESSIONAL' not in row.name
        for options, functions in zip(undergraduate_options, undergraduate_functions):
            if functions(row, odd, options):
                undergraduate_details[options].append(row)

    return undergraduate_details


def show_undergraduate_summary():
    global node_undergraduate
    undergraduate_summary = list()
    node_credit, node_value = defaultdict(lambda: 0.0), defaultdict(lambda: 0.0)
    data_undergraduate = models.Undergraduate.objects.all()

    for row in data_undergraduate:
        if row.grade not in didnt:
            credit = float(row.credit)
            gpa = float(row.gpa)
            node_credit[row.level] += credit
            node_value[row.level] += (credit * gpa)
            node_credit['final'] += credit
            node_value['final'] += (credit * gpa)

    node_undergraduate.append('final')

    for level in node_undergraduate:
        cgpa = (node_value[level] / node_credit[level]) if node_credit[level] else 0
        percentage, grade = get_details_from_cgpa(cgpa)
        node = {
            'level':level,
            'cgpa': f'{cgpa:.2f}',
            'percentage': percentage,
            'grade': grade,
            'credit': f'{node_credit[level]:.2f}'
        }
        undergraduate_summary.append(node)

    return undergraduate_summary


def imonlyhuman_evaluate():
    imonlyhuman_summary = dict()
    average = 0
    data_imonlyhuman = models.Imonlyhuman.objects.all()
    data_imonlyhuman = sorted(data_imonlyhuman, key=lambda i: i.id)

    for row in data_imonlyhuman:
        key = f'{row.classname} / {row.time} / {row.name} : {row.value}'
        imonlyhuman_summary[key] = row.value
        average += int(row.value)

    number_rows = models.Imonlyhuman.objects.count()
    average = int(average / number_rows)
    imonlyhuman_summary[f'imonlyhuman : {average}'] = average
    return imonlyhuman_summary


def analysis_daily():
    global v3rdCurrent, mission, target_hours_daily, week, statistics_days
    data_daily = models.Daily.objects.all()
    data_field = models.Daily._meta.fields
    analysis_summary = {'target_hours_daily': target_hours_daily, 'gone_days': 0, 'gone_hours': 0}

    for row in data_daily:
        for field in data_field:
            name = field.name
            if name == 'id' or name == 'day' or int(getattr(row, name)) == 0:
                continue
            analysis_summary['gone_days'] += 1
            analysis_summary['gone_hours'] += int(getattr(row, name))

    analysis_summary['gone_hours'] = int(analysis_summary['gone_hours'] / 7)
    analysis_summary['average_hours_daily'] = int(analysis_summary['gone_hours'] / analysis_summary['gone_days'])
    analysis_summary['total_hours'] = analysis_summary['gone_days'] * analysis_summary['target_hours_daily']
    analysis_summary['grade'] = int((100 * analysis_summary['gone_hours']) / analysis_summary['total_hours'])
    analysis_summary['mission'] = mission - analysis_summary['gone_hours']

    rdays1 = int(analysis_summary['mission'] / analysis_summary['average_hours_daily'])
    rdays2 = int(analysis_summary['mission'] / week)
    rdays3 = int(analysis_summary['mission'] / analysis_summary['target_hours_daily'])

    analysis_summary['required1st'] = f"{analysis_summary['average_hours_daily']:02d} hours / {rdays1:04d} days"
    analysis_summary['required2nd'] = f"{week:02d} hours / {rdays2:04d} days"
    analysis_summary['required3rd'] = f"{analysis_summary['target_hours_daily']:02d} hours / {rdays3:04d} days"
    return analysis_summary


def _graph_rendering_days(year):
    data_daily = models.Daily.objects.all()
    collection, _collection = dict(), dict()
    for row in data_daily:
        # collection[row.day] = [getattr(row, year), '']
        _collection[row.id] = [row.day, getattr(row, year)]
    number_rows = models.Daily.objects.count()
    for i in range(1, number_rows+1):
        collection[_collection[i][0]] = [_collection[i][1], '']
    return collection


def graph_rendering_days():
    statistics_days = dict()
    for field in models.Daily._meta.fields:
        name = field.name
        if name == 'id' or name == 'day':
            continue
        name = name[1: len(name)]
        statistics_days[name] = _graph_rendering_days(field.name)
    return statistics_days


def _graph_rendering_years(data_x_year, data_field_x, dont_x, check='weight'):
    global statistics_years_details
    for row in data_x_year:
        for field in data_field_x:
            if field.name in dont_x:
                continue
            year = field.name[1:] if check == 'weight' else row.year
            parameter = row.parameter if check == 'weight' else field.name
            value = getattr(row, field.name)
            if year not in statistics_years_details:
                statistics_years_details[year] = dict()
            if parameter not in statistics_years_details[year]:
                statistics_years_details[year][parameter] = list()
            statistics_years_details[year][parameter].append(int(value))


def graph_rendering_years():
    global statistics_years_details
    data_academic = models.Academic.objects.all()
    for row in data_academic:
        if row.year not in statistics_years_details:
            statistics_years_details[row.year] = dict()
        if row.event not in statistics_years_details[row.year]:
            statistics_years_details[row.year][row.event] = list()
        statistics_years_details[row.year][row.event] = [int(row.weight), int(row.value)]

    dont_weight = ['id', 'parameter']

    data_weight_year_a = models.WeightYearA.objects.all()
    data_field_weight_a = models.WeightYearA._meta.fields
    _graph_rendering_years(data_weight_year_a, data_field_weight_a, dont_weight)

    data_weight_year_b = models.WeightYearB.objects.all()
    data_field_weight_b = models.WeightYearB._meta.fields
    _graph_rendering_years(data_weight_year_b, data_field_weight_b, dont_weight)

    dont_value = ['id', 'year', 'event']

    data_value_year_a = models.ValueYearA.objects.all()
    data_field_value_a = models.ValueYearA._meta.fields
    _graph_rendering_years(data_value_year_a, data_field_value_a, dont_value, 'value')

    data_value_year_b = models.ValueYearB.objects.all()
    data_field_value_b = models.ValueYearB._meta.fields
    _graph_rendering_years(data_value_year_b, data_field_value_b, dont_value, 'value')

    statistics_years = dict()
    for year in statistics_years_details:
        x, y = 0, 0
        parameterlist = statistics_years_details[year]
        for parameter in parameterlist:
            weight = int(parameterlist[parameter][0])
            value = int(parameterlist[parameter][1])
            x += (weight * value)
            y += weight
        statistics_years[year] = math.ceil(x / y)
    return statistics_years


undergraduate_details = show_undergraduate_details()
undergraduate_summary = show_undergraduate_summary()
analysis_summary = analysis_daily()
imonlyhuman_summary = json.dumps(imonlyhuman_evaluate())
statistics_days = json.dumps(graph_rendering_days())
statistics_years = graph_rendering_years()

context = {
    'v1stStart': v1stStart, 'v2ndLast': v2ndLast, 'v3rdCurrent': v3rdCurrent,
    'undergraduate_details': undergraduate_details,
    'undergraduate_summary': undergraduate_summary,
    'analysis_summary': analysis_summary,
    'imonlyhuman_summary': imonlyhuman_summary,
    'statistics_days': statistics_days,
    'statistics_years': statistics_years,
    'statistics_years_details': statistics_years_details,
}


def views_index(request):
    global context
    return render(request, 'index.html', context)


def views_main(request):
    global context
    return render(request, 'main.html', context)


def views_main_undergraduate_details(request):
    global context
    undergraduate_details_specified = undergraduate_details[request.GET.get('options')]
    context['undergraduate_details_specified'] = undergraduate_details_specified
    return render(request, 'main_undergraduate_details.html', context)


def views_main_undergraduate_summary(request):
    global context
    return render(request, 'main_undergraduate_summary.html', context)


def views_main_analysis(request):
    global context
    return render(request, 'main_analysis.html', context)
