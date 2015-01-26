courses = [
	
	('ARCH', 201, 'Intro to Architecture'),
	('ARCH', 381, 'Architectural Des I'),
	('CIS',210, 'Computer Science I'),
	('CIS', 315, 'Data Structures'),
	('CIS', 451, 'Databases'),
	('FR', 101, '1st Year French'),
	('FR', 201, '2nd Year French'),
	('BA', 101, 'Intro to Business'),
	('BA', 215, 'Lang of Bus Decision'),
	('BI', 211, 'Gen Biol I: Cells'),
	('BI',130, 'Intro to Ecology'),
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
('ED',75),
('LIL',55),
('LA',160),
('DES',200),
('FEN',100),
('FEN', 205),
('LLC',160),
('ALL',025),
('KLA',026),
('PAC',110),
('GER',210)]


instructors =[
	'Chris Wilson', #cis
	'Michal Young', #CIS
	'Steve Engel', #ARCH
	'Shannon Doyle', #ARCH
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



#subject_code, number, credits, room, bldg,  days, instructor_name
offerings = [
	('ARCH', 201,5.00,'LA', 160,'tr', 'Steve Engel'),
	('ARCH', 381,5.00, 'LA', 160, 'mw', 'Shannon Doyle'), 
	('CIS',210,4.00, 'LLC', 160, 'mtwr', 'Michal Young' ),
	('CIS', 451, 4.00,   'ALL', 25, 'mwf', 'Chris Wilson'), 
	('FR', 101, 4.00, 'PAC', 110, 'mtw', 'Constance Dickey'),
	('FR', 201, 4.00, 'PAC',110, 'tr','Constance Dickey'),
	('BA', 101, 4.00, 'LIL', 55, 'm', 'Anthony Tridbit' ),
	('BA', 215, 4.00, 'LIL', 55, 'wf', 'April Haynes'),
	('BI', 211, 'KLA',26,'mwrf', 'Vince Lombardi'),	
	('SPAN', 101,4.00,'PAC',110,'mtwrf','Inaki Gonzalo'),
	('SPAN', 201,4.00, 'PAC',110,'mtwrf','Inaki Gonzalo'), 
	('HIST', 121,4.00, 'ED',75, 'mwf', 'Matt Dennis'), 
	('HIST', 201,4.00, 'ED', 75, 'mwf', 'Matt Dennis'), 
	('PHYS', 251,4.00, 'KLA', 22, 'mwf', 'Eric Torrence'), 
	('PHYS', 252,4.00, 'KLA', 22, 'mwf', 'Eric Torrence'), 
	('MATH', 231,4.00, 'FEN', 100, 'tr', 'Boris Botanvick'), 
	('MATH', 315,4.00, 'FEN', 205, 'wr', 'Sasha Pochinski'), 
	('ART', 115, 4.00,'GER', 210 , 'mwf', 'Tyrras Warren'), 
	('ART', 116, 4.00,'GER', 210, 'tr', 'Tyrras Warren'), 
	('CIS',315,4.00,'ED',75,12345,'mw','Chris Wilson'),
	('CIS',315,4.00,'DES',200,12344, 'tr','Andrezj P'),
	('ARCH',281,5.00,'LA',55,12333,'mwf','Steve Engel'),
	]