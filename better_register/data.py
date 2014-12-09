courses = [

    ('ARCH', 201, 'Intro to Architecture'),
    ('ARCH', 381, 'Architectural Des I'),
    ('CIS', 210, 'Computer Science I'),
    ('CIS', 315, 'Data Structures'),
    ('CIS', 451, 'Databases'),
    ('FR', 101, '1st Year French'),
    ('FR', 201, '2nd Year French'),
    ('BA', 101, 'Intro to Business'),
    ('BA', 215, 'Lang of Bus Decision'),
    ('BI', 211, 'Gen Biol I: Cells'),
    ('BI', 130, 'Intro to Ecology'),
    ('SPAN', 101, '1st Year Spanish'),
    ('SPAN', 201, '2nd Year Spanish'),
    ('HIST', 121, 'Women in World History'),
    ('HIST', 201, 'United States'),
    ('PHYS', 251, 'Foundations of Physics I'),
    ('PHYS', 252, 'Foundations of Physics II'),
    ('PHYS', 252, 'Foundations of Physics III'),
    ('MATH', 231, 'Discrete Math I'),
    ('MATH', 315, 'Elementary Analysis'),
    ('ART', 115, 'Surface, Space, & Time'),
    ('ART', 116, 'Core Interdis Lab')
]

locations = [
    ('ED', 75),
    ('LIL', 55),
    ('LA', 160),
    ('DES', 200),
    ('FEN', 100),
    ('FEN', 205),
    ('LLC', 160),
    ('ALL', 25),
    ('KLA', 26),
    ('PAC', 110),
    ('GER', 210)]

instructors = [
    'Chris Wilson',  # cis
    'Michal Young',  #CIS
    'Steve Engel',  #ARCH
    'Shannon Doyle',  #ARCH
    'Constance Dickey',
    'Andrezj P',
    'Anthony Tridbit',
    'Vince Lombardi',
    'April Haynes',
    'Matt Dennis',
    'Eric Torrence',
    'Boris Botanvick',
    'Sasha Pochinski',
    'Paul Elliot',
    'Daniel Ellsworth',
]



# subject_code, number, credits, room, bldg,  days, instructor_name
evals = [
    ('ARCH', 201, 'Steve Engel', 3),
    ('ARCH', 381, 'Shannon Doyle', 4),
    ('CIS', 210, 'Michal Young', 5 ),
    ('CIS', 451, 'Chris Wilson', 5),
    ('FR', 101, 'Constance Dickey', 4),
    ('FR', 201, 'Constance Dickey', 3),
    ('BA', 101, 'Anthony Tridbit', 1),
    ('BA', 215, 'April Haynes', 2),
    ('BI', 211, 'Vince Lombardi', 4),
    ('SPAN', 101, 'Inaki Gonzalo', 3),
    ('SPAN', 201, 'Inaki Gonzalo', 3),
    ('HIST', 121, 'Matt Dennis', 2),
    ('HIST', 201, 'Matt Dennis', 2),
    ('PHYS', 251, 'Eric Torrence', 4),
    ('PHYS', 252, 'Eric Torrence', 4),
    ('MATH', 231, 'Boris Botanvick', 2),
    ('MATH', 315, 'Sasha Pochinski', 3),
    ('ART', 115, 'Tyrras Warren', 2),
    ('ART', 116, 'Tyrras Warren', 4),
    ('CIS', 315, 'Chris Wilson', 5),
    ('CIS', 315, 'Andrezj P', 2)
]

offerings = [('ARCH', 201,'LA',160, 'tr', 'Steve Engel'),
             ('ARCH', 381,'LA',160, 'mw', 'Shannon Doyle'),
             ('CIS', 210, 'LLC', 160, 'mtwr', 'Michal Young' ),
             ('CIS', 451, 'ALL', 25, 'mwf', 'Chris Wilson'),
('FR', 101, 'PAC',110, 'mtw', 'Constance Dickey'),
('FR', 201, 'PAC',110, 'tr', 'Constance Dickey'),
('BA', 101, 'LIL', 55, 'm', 'Anthony Tridbit' ),
('BA', 215, 'LIL', 55, 'wf', 'April Haynes'),
('BI', 211, 'KLA', 26, 'mwrf', 'Vince Lombardi'),
('SPAN', 101, 'PAC',110,'mtwrf', 'Inaki Gonzalo'),
('SPAN', 201, 'PAC',110, 'mtwrf', 'Inaki Gonzalo'),
('HIST', 121, 'ED', 75, 'mwf', 'Matt Dennis'),
('HIST', 201, 'ED', 75, 'mwf', 'Matt Dennis'),
('PHYS', 251, 'KLA', 26, 'mwf', 'Eric Torrence'),
('PHYS', 252, 'KLA', 26, 'mwf', 'Eric Torrence'),
('MATH', 231, 'FEN', 100, 'tr', 'Boris Botanvick'),
('MATH', 315, 'FEN', 205, 'wr', 'Sasha Pochinski'),
('ART', 115, 'GER', 210, 'mwf', 'Tyrras Warren'),
('ART', 116, 'GER', 210, 'tr', 'Tyrras Warren'),
('CIS', 315, 'ED', 75,  'mw', 'Chris Wilson'),
('CIS', 315, 'DES', 200, 'tr', 'Andrezj P'),]