insert into dept (name, budget) values
('Computer Science', 500000),
('Math', 300000),
('Statistics', 400000);

insert into building (name) values
('AB'),
('WDR'),
('IB'),
('LIB'),
('CCT'),
('TBA');

insert into classroom (building_name, room_name) values
('AB', '1079'),
('AB', '1087'),
('AB', '2107'),
('AB', '3101'),
('AB', '3103'),
('WDR', '1100'),
('WDR', '1007'),
('WDR', '1003'),
('WDR', '1005'),
('IB', '3106'),
('IB', '2071'),
('IB', '2050'),
('IB', '2028'),
('IB', '2025'),
('IB', '2001'),
('IB', '1056'),
('IB', '1052'),
('IB', '1047'),
('IB', '1046'),
('IB', '1017'),
('IB', '1012'),
('IB', '1011'),
('LIB', '1119'),
('LIB', '1123'),
('LIB', '2113'),
('LIB', '2115'),
('CCT', 'E1011'),
('CCT', 'E2011'),
('TBA', 'TBA');


insert into student (id, first_name, last_name, major, class) values 
('yg202', 'Yinuo', 'Guo', 'Art History', '2025'),
('jc923', 'Jingfeng', 'Chen', 'Computer Science', '2026'),
('jq48', 'Jason', 'Qiu', 'Computer Science', '2026');

insert into instructor (id, first_name, last_name, dept, salary, isDuke) values 
('mm940', 'Mustafa', 'Misir', 'Computer Science', 1, False),
('bl291', 'Bing', 'Luo', 'Computer Science', 100000, False),
('dl288', 'Daniel', 'Lim', 'Computer Science', 100000, True),
('yg281', 'Yuxuan', 'Gao', 'Computer Science', 50000, False),
('ft47', 'Feng', 'Tian', 'Computer Science', 100000, False),
('xc171', 'Xingshi', 'Cai', 'Computer Science', 100000, False),
('mh596', 'Ming-Chun', 'Huang', 'Computer Science', 100000, False),
('js1242', 'Jiacheng', 'Shen', 'Computer Science', 100000, False),
('ps298', 'Peng', 'Sun', 'Computer Science', 100000, False),
('dc383', 'Dangxing', 'Chen', 'Math', 100000, True),
('zh148', 'Zhenghui', 'Huo', 'Math', 100000, True),
('dz95', 'Dongmian', 'Zou', 'Math', 100000, True),
('sx59', 'Shixin', 'Xu', 'Math', 100000, False),
('ke83', 'Konstantinos', 'Efstathiou', 'Math', 100000, False),
('pjg32', 'Pascal', 'Grange', 'Math', 100000, True),
('lj176', 'Lin', 'Jiu', 'Math', 100000, True),
('mw170', 'Marcus', 'Werner', 'Math', 100000, True),
('jl164', 'Jian-Guo', 'Liu', 'Math', 100000, True),
('hh321', 'Huaxiong', 'Huang', 'Math', 100000, True),
('pg180', 'Pengzhan', 'Guo', 'Math', 100000, True),
('is124', 'Italo', 'Simonelli', 'Math', 100000, True),
('awm31', 'Andrew', 'MacDonald', 'Statistics', 100000, True),
('mn279', 'Markus', 'Neumann', 'Statistics', 100000, True),
('ml442', 'Ming', 'Li', 'Statistics', 100000, False),
('lz183', 'Luyao', 'Zhang', 'Statistics', 100000, False),
('pw160', 'Paul', 'Wang', 'Statistics', 100000, False),
('cv127', 'Cristiano', 'Villa', 'Statistics', 100000, False),
('yj232', 'Yucheng', 'Jin', 'Statistics', 100000, False),
('jy313', 'Jiahua', 'Yue', 'Statistics', 100000, True);

insert into advised (student_id, advisor_id) values 
('yg202', 'mm940'),
('jc923', 'dc383'),
('jq48', 'mm940');



insert into course (id, type, name, description, dept_name, credits) values 
('COMPSCI 101', 'SEM', 'Introduction to Computer Science', 'As an introductory course for computer science, this course will bring you not only the fundamental knowledge on a variety of CS topics, but also the essential computational problem-solving skills with hands on programming experience. Successfully completing this course will serve a solid foundation for other courses in the computer science or data science major. It can also bring new concepts and tools to other domains in social science, arts humanities and natural science. This course is an elective course open to everyone, and no specific prerequisite required.',
'Computer Science', 4.0),
('COMPSCI 101', 'LAB', 'Introduction to Computer Science', 'As an introductory course for computer science, this course will bring you not only the fundamental knowledge on a variety of CS topics, but also the essential computational problem-solving skills with hands on programming experience. Successfully completing this course will serve a solid foundation for other courses in the computer science or data science major. It can also bring new concepts and tools to other domains in social science, arts humanities and natural science. This course is an elective course open to everyone, and no specific prerequisite required.',
'Computer Science', 0),
('COMPSCI 201', 'SEM', 'Introduction to Programming and Data Structures', 'This course covers data and representations, functions, conditions, loops, strings, lists, sets, maps, hash tables, trees, stacks, graphs, object-oriented programming, programming interface and software engineering.',
'Computer Science', 4.0),
('COMPSCI 201', 'LAB', 'Introduction to Programming and Data Structures', 'This course covers data and representations, functions, conditions, loops, strings, lists, sets, maps, hash tables, trees, stacks, graphs, object-oriented programming, programming interface and software engineering.',
'Computer Science', 0),
('COMPSCI 201', 'REC', 'Introduction to Programming and Data Structures', 'This course covers data and representations, functions, conditions, loops, strings, lists, sets, maps, hash tables, trees, stacks, graphs, object-oriented programming, programming interface and software engineering.',
'Computer Science', 0),
('COMPSCI 203', 'LEC', 'Discrete Math for Computer Science', 'This course focuses on the following: mathematical notations, logic, and proof; linear and matrix algebra; graphs, digraphs, trees, representations, and algorithms; counting, permutations, combinations, discrete probability, Markov models; advanced topics from algebraic structures, geometric structures, combinatorial optimization, number theory.',
'Computer Science', 4.0),
('COMPSCI 203', 'REC', 'Discrete Math for Computer Science', 'This course focuses on the following: mathematical notations, logic, and proof; linear and matrix algebra; graphs, digraphs, trees, representations, and algorithms; counting, permutations, combinations, discrete probability, Markov models; advanced topics from algebraic structures, geometric structures, combinatorial optimization, number theory.',
'Computer Science', 0),
('COMPSCI 205', 'SEM', 'Computer Organization and Programming', 'This course focuses on the following: computer structure, assembly language, instruction execution, addressing techniques, and digital representation of data. Computer system organization, logic design, microprogramming, cache and memory systems, and input/output interfaces are also central.',
'Computer Science', 4.0),
('COMPSCI 205', 'REC', 'Computer Organization and Programming', 'This course focuses on the following: computer structure, assembly language, instruction execution, addressing techniques, and digital representation of data. Computer system organization, logic design, microprogramming, cache and memory systems, and input/output interfaces are also central.',
'Computer Science', 0),
('COMPSCI 207', 'SEM', 'Image Data Science', 'This course introduces the logical structure of digital media and explores computational media manipulation. The course uses the Python programming language to explore media manipulation and transformation. Topics include spatial and temporal resolution, color, texture, filtering, compression and feature detection.',
'Computer Science', 4.0),
('COMPSCI 301', 'SEM', 'Algorithms and Databases', 'This course covers sorting, order statistics, binary search, dynamic programming, greedy algorithms, graph algorithms, minimum spanning trees, shortest paths, SQL, file organization, hashing, sorting, query, schema, transaction management, concurrency control, rash recovery, distributed database, and database as a service.',
'Computer Science', 4.0),
('COMPSCI 301', 'REC', 'Algorithms and Databases', 'This course covers sorting, order statistics, binary search, dynamic programming, greedy algorithms, graph algorithms, minimum spanning trees, shortest paths, SQL, file organization, hashing, sorting, query, schema, transaction management, concurrency control, rash recovery, distributed database, and database as a service.',
'Computer Science', 0),
('COMPSCI 308', 'SEM', 'Design and Analysis of Algorithms', 'This course focuses on the design and analysis of efficient algorithms including sorting, searching, dynamic programming, graph algorithms, fast multiplication, and others. It also includes nondeterministic algorithms and computationally hard problems.',
'Computer Science', 4.0),
('COMPSCI 308', 'REC', 'Design and Analysis of Algorithms', 'This course focuses on the design and analysis of efficient algorithms including sorting, searching, dynamic programming, graph algorithms, fast multiplication, and others. It also includes nondeterministic algorithms and computationally hard problems.',
'Computer Science', 0),
('COMPSCI 309', 'SEM', 'Principles of Machine Learning', 'This course covers maximum likelihood estimation, linear discriminant analysis, logistic regression, support vector machine, decision tree, linear regression, Bayesian inference, unsupervised learning, and semi-supervised learning. Students are not allowed to take both MATH 405 and STATS 302 because of the content overlap. Students who are planning to major in Data Science should take STATS 302.',
'Computer Science', 4.0),
('COMPSCI 309', 'REC', 'Principles of Machine Learning', 'This course covers maximum likelihood estimation, linear discriminant analysis, logistic regression, support vector machine, decision tree, linear regression, Bayesian inference, unsupervised learning, and semi-supervised learning. Students are not allowed to take both MATH 405 and STATS 302 because of the content overlap. Students who are planning to major in Data Science should take STATS 302.',
'Computer Science', 0),
('COMPSCI 310', 'LEC', 'Introduction of Databases', 'This course focuses on databases and relational database management systems. It includes data modeling, database design theory, data definition and manipulation languages, storaging and indexing techniques, query processing and optimization, concurrency control and recovery, database programming interfaces. Current research issues including XML, web data management, data integration and dissemination, data mining are also considered. Hands-on programming projects and a term project.',
'Computer Science', 4.0),
('COMPSCI 402', 'SEM', 'Artificial Intelligence', 'This course covers uninformed search, informed search, constraint satisfaction, classical planning, neural network, deep learning, hidden Markov model, Bayesian network, Markov decision process, reinforcement learning, active learning and game theory.',
'Computer Science', 4.0),
('Math 101', 'LEC', 'Introductory Calculus', 'This course offers an introduction to Calculus, a subject that is the foundation for a large part of modern mathematics and has countless applications across the sciences and beyond. The course covers the fundamental Calculus concepts (limits, continuity, differentiation, integration) and explores related applications. The treatment of these concepts assumes no prior knowledge of Calculus. Recommended for students who have not had a previous (high-school level) Calculus course. Students who have had such a Calculus course are recommended to take MATH 105 instead.',
'Math', 4.0),
('Math 101', 'REC', 'Introductory Calculus', 'This course offers an introduction to Calculus, a subject that is the foundation for a large part of modern mathematics and has countless applications across the sciences and beyond. The course covers the fundamental Calculus concepts (limits, continuity, differentiation, integration) and explores related applications. The treatment of these concepts assumes no prior knowledge of Calculus. Recommended for students who have not had a previous (high-school level) Calculus course. Students who have had such a Calculus course are recommended to take MATH 105 instead.',
'Math', 0),
('Math 105', 'LEC', 'Calculus', 'Calculus is the foundation for a large part of modern mathematics and has countless applications across the sciences and beyond. This course covers the fundamental Calculus concepts (limits, continuity, differentiation, integration) and explores related applications. The treatment of these concepts assumes some prior knowledge of Calculus. Recommended for students who have had a previous (high-school level) Calculus course. Students who have not had such a Calculus course are recommended to take MATH 101 instead.',
'Math', 4.0),
('Math 105', 'REC', 'Calculus', 'Calculus is the foundation for a large part of modern mathematics and has countless applications across the sciences and beyond. This course covers the fundamental Calculus concepts (limits, continuity, differentiation, integration) and explores related applications. The treatment of these concepts assumes some prior knowledge of Calculus. Recommended for students who have had a previous (high-school level) Calculus course. Students who have not had such a Calculus course are recommended to take MATH 101 instead.',
'Math', 0),
('MATH 201', 'SEM', 'Multivariable Calculus', "Main topics of this course include vectors and vector functions, the geometry of higher dimensional Euclidean spaces, partial derivatives, multiple integrals, line integrals, vector fields, Green’s Theorem, Stokes’ Theorem and the Divergence Theorem.",
'Math', 4.0),
('MATH 201', 'REC', 'Multivariable Calculus', "Main topics of this course include vectors and vector functions, the geometry of higher dimensional Euclidean spaces, partial derivatives, multiple integrals, line integrals, vector fields, Green’s Theorem, Stokes’ Theorem and the Divergence Theorem.",
'Math', 0),
('MATH 202', 'SEM', 'Linear Algebra', 'Systems of linear equations and elementary row operations, Euclidean n-space and subspaces, linear transformations and matrix representations, Gram-Schmidt orthogonalization process, determinants, eigenvectors and eigenvalues; applications.',
'Math', 4.0),
('MATH 202', 'REC', 'Linear Algebra', 'Systems of linear equations and elementary row operations, Euclidean n-space and subspaces, linear transformations and matrix representations, Gram-Schmidt orthogonalization process, determinants, eigenvectors and eigenvalues; applications.',
'Math', 0),
('Math 203', 'LEC', 'Advanced Calculus', 'Sequences, series, and their convergence properties. Power series, Taylor series, and Fourier series. Solution methods for first and second order differential equations.',
'Math', 4.0),
('Math 203', 'REC', 'Advanced Calculus', 'Sequences, series, and their convergence properties. Power series, Taylor series, and Fourier series. Solution methods for first and second order differential equations.',
'Math', 0),
('MATH 205', 'LEC', 'Probability and Statistics', 'The course begins with a brief overview of sequences and series followed by an introduction to probability theory and statistics. It covers basic concepts of probability, independence, conditional probability, random variables, with emphasis on probability distributions that frequently arise in applications. Convergence in distribution and convergence in probability; the central limit theorem, and the weak law of large numbers. Topics from classical statistics, and introduction to linear regression.',
'Math', 4.0),
('MATH 205', 'REC', 'Probability and Statistics', 'The course begins with a brief overview of sequences and series followed by an introduction to probability theory and statistics. It covers basic concepts of probability, independence, conditional probability, random variables, with emphasis on probability distributions that frequently arise in applications. Convergence in distribution and convergence in probability; the central limit theorem, and the weak law of large numbers. Topics from classical statistics, and introduction to linear regression.',
'Math', 0),
('MATH 206', 'LEC', 'Probability and Statistics', 'This course serves as an introduction to probability theory and statistics. It covers basic concepts of probability, independence, conditional probability, random variables, with emphasis on probability distributions that frequently arise in applications. Convergence in distribution and convergence in probability; the central limit theorem, and the weak law of large numbers. Topics from classical and Bayesian statistics, and introduction to linear regression.',
'Math', 4.0),
('MATH 206', 'REC', 'Probability and Statistics', 'This course serves as an introduction to probability theory and statistics. It covers basic concepts of probability, independence, conditional probability, random variables, with emphasis on probability distributions that frequently arise in applications. Convergence in distribution and convergence in probability; the central limit theorem, and the weak law of large numbers. Topics from classical and Bayesian statistics, and introduction to linear regression.',
'Math', 0),
('Math 302', 'SEM', 'Numerical Analysis', 'Introductory course on numerical analysis. Topics include: Development of numerical techniques for accurate, efficient solution of problems in science, engineering, and mathematics through the use of computers. Linear systems, nonlinear equations, optimization, numerical integration, differential equations, simulation of dynamical systems, error analysis. Students are not allowed to take both MATH 302 and MATH 304 because of the content overlap. Students who are planning to major in Data Science should take MATH 304 instead, and those who have taken MATH 302 may not major in Data Science.',
'Math', 4.0),
('Math 302', 'LAB', 'Numerical Analysis', 'Introductory course on numerical analysis. Topics include: Development of numerical techniques for accurate, efficient solution of problems in science, engineering, and mathematics through the use of computers. Linear systems, nonlinear equations, optimization, numerical integration, differential equations, simulation of dynamical systems, error analysis. Students are not allowed to take both MATH 302 and MATH 304 because of the content overlap. Students who are planning to major in Data Science should take MATH 304 instead, and those who have taken MATH 302 may not major in Data Science.',
'Math', 0),
('Math 303', 'SEM', 'ODE and Dynamical Systems', 'Theory of ordinary differential equations with some of the modern theory of dynamical systems. Topics include differential equations and linear systems of DEs, the general theory of nonlinear systems, the qualitative behavior of two-dimensional and higher-dimensional systems, and applications in various areas.',
'Math', 4.0),
('Math 304', 'SEM', 'Numerical Analysis and Optimization', 'This course covers Gaussian elimination, LU factorization, Cholesky decomposition, QR decomposition, Newton-Raphson method, binary search, convex function, convex set, gradient method, Newton method, Lagrange dual, KKT condition, interior point method, conjugate gradient method, random walk, and stochastic optimization. Students are not allowed to take both MATH 302 and MATH 304 because of the content overlap. Students who are planning to major in Applied Math and Computational Sciences should take MATH 302 instead, and those who have taken MATH 304 may not major in Applied Math and Computational Sciences.',
'Math', 4.0),
('Math 304', 'REC', 'Numerical Analysis and Optimization', 'This course covers Gaussian elimination, LU factorization, Cholesky decomposition, QR decomposition, Newton-Raphson method, binary search, convex function, convex set, gradient method, Newton method, Lagrange dual, KKT condition, interior point method, conjugate gradient method, random walk, and stochastic optimization. Students are not allowed to take both MATH 302 and MATH 304 because of the content overlap. Students who are planning to major in Applied Math and Computational Sciences should take MATH 302 instead, and those who have taken MATH 304 may not major in Applied Math and Computational Sciences.',
'Math', 0),
('Math 305', 'SEM', 'Advanced Linear Algebra', 'This course covers pseudo inverse, inner product, vector spaces and subspaces, orthogonality, linear transformations and operators, projections, matrix factorization, and singular value decomposition. COMPSCI 201 or COMPSCI 101 or STATS 102 is recommended',
'Math', 4.0),
('Math 305', 'REC', 'Advanced Linear Algebra', 'This course covers pseudo inverse, inner product, vector spaces and subspaces, orthogonality, linear transformations and operators, projections, matrix factorization, and singular value decomposition. COMPSCI 201 or COMPSCI 101 or STATS 102 is recommended',
'Math', 0),
('Math 307', 'SEM', 'Complex Analysis', 'Introduction to analysis of functions of complex variables. Topics include complex numbers, analytic functions, complex integration, Taylor and Laurent series, theory of residues, argument and maximum principles, conformal mapping.',
'Math', 4.0),
('Math 308', 'SEM', 'Real Analysis', 'The course discusses the defining properties of the real numbers, the topology of the real line and its subsets, and a rigorous development of single variable Calculus including limits, sequences and series of numbers, continuity, differentiability, sequences and series of functions, the power series representation of functions, and the Riemann integral, culminating in the Fundamental Theorem of Calculus. This is an abstract mathematics course with a heavy emphasis on proofs and formal arguments rather than on computations. Even though not strictly required, it is strongly suggested that students take MATH 201 or MATH 202 before taking MATH 308.',
'Math', 4.0),
('MATH 405', 'SEM', 'Mathematics of Data Analysis and Machine Learning', 'Geometry of high dimensional data sets. Linear dimension reduction, principal component analysis, kernel methods. Nonlinear dimension reduction, manifold models. Graphs. Random walks on graphs, diffusions, page rank. Clustering, classification and regression in high- dimensions. Sparsity. Computational aspects, randomized algorithms.',
'Math', 4.0),
('Math 407', 'LEC', 'General Relativity', 'Introduction to tensor calculus and metric geometry; Maxwell theory and special relativity; Lorentzian spacetimes; Einstein field equations; Schwarzschild and Kerr solutions, black hole properties; Friedmann equations and cosmology; optical geometry and gravitational lensing; gravitational waves; current research overview',
'Math', 4.0),
('Math 408', 'SEM', 'Differential Geometry', 'A first course to differential geometry focusing on the study of curves and surfaces in 2- and 3-dimensional Euclidean space using the techniques of differential and integral calculus and linear algebra. Topics include curvature and torsion of curves, Frenet-Serret frames, global properties of closed curves, intrinsic and extrinsic properties of surface, Gaussian curvature and mean curvatures, geodesics, minimal surfaces, and the Gauss-Bonnet theorem.',
'Math', 4.0),
('Math 412', 'LEC', 'Functional Analysis', 'This course will cover topics including normed spaces, functionals, operators, and major theorems (Banach-Alaoglu theorem, uniform boundedness theorem, open mapping theorem, Hahn-Banach theorem, spectral theory for compact operator) in functional analysis as well as their applications. It will concentrate on the topological and infinite dimensional structure of function spaces, with examples in Fourier analysis, as an extension of linear algebra, and in applications in mathematical analysis. Prerequisites: MATH 202 and MATH 308. MATH 409 Topology and MATH 450 Measure Theory and Integration are also recommended.',
'Math', 4.0),
('Math 450', 'SEM', 'Measure and Integration', 'Introduction to analysis of functions of real variables. Topics include Lebesgue measure and integration; L^p spaces; absolute continuity; abstract measure theory; Radon-Nikodym Theorem; connection with probability; Fourier series and integrals.',
'Math', 4.0),
('STATS 101', 'LEC', 'Introduction to Applied Statistical Methods', 'This course will introduce students to common statistics used in social science research articles and the media with the goal of making them informed and critical consumers of research results reported by various sources. Students will gain understanding of the conceptual basis and purpose of different statistics, as well as the formulas for deriving them. The relationship of statistical analysis to other components of the research process will be explicated. The course will be taught using team-based learning with an emphasis on the application of new concepts, knowledge, and skills in the classroom. Application activities will include interpreting statistics presented in tables and graphics in research articles and the media, critiquing conclusions drawn from statistics, and using statistical software, such as SPSS or Stata, to conduct statistical tests and generate tables and graphics.',
'Statistics', 4.0),
('STATS 101', 'LAB', 'Introduction to Applied Statistical Methods', 'This course will introduce students to common statistics used in social science research articles and the media with the goal of making them informed and critical consumers of research results reported by various sources. Students will gain understanding of the conceptual basis and purpose of different statistics, as well as the formulas for deriving them. The relationship of statistical analysis to other components of the research process will be explicated. The course will be taught using team-based learning with an emphasis on the application of new concepts, knowledge, and skills in the classroom. Application activities will include interpreting statistics presented in tables and graphics in research articles and the media, critiquing conclusions drawn from statistics, and using statistical software, such as SPSS or Stata, to conduct statistical tests and generate tables and graphics.',
'Statistics', 0),
('STATS 102', 'LEC', 'Introduction to Data Science', 'As an introductory course in data science, this course will show students not only the big picture of data science but also the detailed essential skills of loading, cleaning, manipulating, visualizing, analyzing and interpreting data with hands on programming experience. Not open to students who have credit for COMPSCI 101.',
'Statistics', 4.0),
('STATS 102', 'LAB', 'Introduction to Data Science', 'As an introductory course in data science, this course will show students not only the big picture of data science but also the detailed essential skills of loading, cleaning, manipulating, visualizing, analyzing and interpreting data with hands on programming experience. Not open to students who have credit for COMPSCI 101.',
'Statistics', 0),
('STATS 201', 'SEM', 'Introduction to Machine Learning for Social Science', 'In almost every field, there is a need to draw inference from or make decisions based on data. The goal of this course is to provide an introduction to machine learning that is approachable to diverse disciplines and empowers students to become proficient in the foundational concepts and tools while working with interdisciplinary real-world data. You will learn to (a) structure a machine learning problem, (b) determine which algorithmic tools are applicable to a given problem, (c) apply those algorithmic tools to diverse, interdisciplinary data examples, (d) evaluate the performance of your solution, and (e) how to accurately interpret and communicate your results. This course is a fast-paced, applied introduction to machine learning that arms you with the basic skills you will need in practice to both conduct analyses and effectively communicate your results.',
'Statistics', 4.0),
('STATS 202', 'LEC', 'Modeling and Predicting', 'Across a wide array of settings and problems, models are employed to predict future outcomes. This course develops a conceptual overview, linked to real world cases across a wide range of domains, of the challenges involved in predicting the future. “Reduced form” approaches that employ data to predict based on past patterns are distinguished from “structural” approaches that allow data to influence parameters in domain-based theoretical models used to simulate counterfactuals. The strengths and weaknesses of each approach will be investigated with an aim of developing key intuitions about how data and domain knowledge shape the ways in which prediction can unfold — and the balance of approaches that is most appropriate depending on the underlying questions asked in different settings. Having previously completed COMPSCI 101 or STATS 102 or INFOSCI 102 is recommended but not required.',
'Statistics', 4.0),
('STATS 202', 'LAB', 'Modeling and Predicting', 'Across a wide array of settings and problems, models are employed to predict future outcomes. This course develops a conceptual overview, linked to real world cases across a wide range of domains, of the challenges involved in predicting the future. “Reduced form” approaches that employ data to predict based on past patterns are distinguished from “structural” approaches that allow data to influence parameters in domain-based theoretical models used to simulate counterfactuals. The strengths and weaknesses of each approach will be investigated with an aim of developing key intuitions about how data and domain knowledge shape the ways in which prediction can unfold — and the balance of approaches that is most appropriate depending on the underlying questions asked in different settings. Having previously completed COMPSCI 101 or STATS 102 or INFOSCI 102 is recommended but not required.',
'Statistics', 0),
('STATS 210', 'SEM', 'Probability, Random Variables and Stochastic Processes', 'This course covers probability models, random variables with discrete and continuous distributions, independence, joint distributions, conditional distributions, expectations, functions of random variables, central limit theorem, stochastic processes, random walks, and Markov chains. COMPSCI 201 or COMPSCI 101 or STATS 102 is recommended.',
'Statistics', 4.0),
('STATS 210', 'REC', 'Probability, Random Variables and Stochastic Processes', 'This course covers probability models, random variables with discrete and continuous distributions, independence, joint distributions, conditional distributions, expectations, functions of random variables, central limit theorem, stochastic processes, random walks, and Markov chains. COMPSCI 201 or COMPSCI 101 or STATS 102 is recommended.',
'Statistics', 0),
('STATS 211', 'LEC', 'Introduction to Stochastic Processes', 'The course begins with a brief overview of sequences and series followed by an introduction to stochastic processes and applications. Several examples of stochastic processes are covered: Markov chains, random walks, branching processes, the Poisson process, and Brownian motion.',
'Statistics', 4.0),
('STATS 211', 'REC', 'Introduction to Stochastic Processes', 'The course begins with a brief overview of sequences and series followed by an introduction to stochastic processes and applications. Several examples of stochastic processes are covered: Markov chains, random walks, branching processes, the Poisson process, and Brownian motion.',
'Statistics', 0),
('STATS 302', 'SEM', 'Principles of Machine Learning', 'This course covers maximum likelihood estimation, linear discriminant analysis, logistic regression, support vector machine, decision tree, linear regression, Bayesian inference, unsupervised learning, and semi-supervised learning. Students are not allowed to take both MATH 405 and STATS 302 because of the content overlap. Students who are planning to major in Data Science should take STATS 302.',
'Statistics', 4.0),
('STATS 302', 'REC', 'Principles of Machine Learning', 'This course covers maximum likelihood estimation, linear discriminant analysis, logistic regression, support vector machine, decision tree, linear regression, Bayesian inference, unsupervised learning, and semi-supervised learning. Students are not allowed to take both MATH 405 and STATS 302 because of the content overlap. Students who are planning to major in Data Science should take STATS 302.',
'Statistics', 0),
('STATS 303', 'SEM', 'Statistical Machine Learning', 'This course covers statistical inference, parametric method, sparsity, nonparametric methods, learning theory, kernel methods, computation algorithms and advanced learning topics.',
'Statistics', 4.0),
('STATS 303', 'REC', 'Statistical Machine Learning', 'This course covers statistical inference, parametric method, sparsity, nonparametric methods, learning theory, kernel methods, computation algorithms and advanced learning topics.',
'Statistics', 0),
('STATS 401', 'SEM', 'Data Acquisition and Visualization', 'This course introduces the principles and methodologies for data acquisition and visualization, along with tools and techniques used to clean and process data for visual analysis. It also covers the practical software tools and languages such as Tableau, OpenRefine and Python/Matlab.',
'Statistics', 4.0),
('STATS 402', 'SEM', 'Interdisciplinary Data Analysis', 'This course covers interdisciplinary applications of data analysis for social science, behavioral modeling, health care, financial modeling, advanced manufacturing, etc. Students are expected to solve a number of practical problems by implementing data algorithms with R during their course projects.',
'Statistics', 4.0);

insert into section (course_id, type, term, session, year, capacity, building_name, room_name) values 
('COMPSCI 101', 'SEM', 'Fall', 'first', 2024, 60, 'AB', '1079'),
('COMPSCI 101', 'LAB', 'Fall', 'first', 2024, 30, 'AB', '3103'),
('COMPSCI 101', 'LAB', 'Fall', 'first', 2024, 30, 'AB', '3103'),
('COMPSCI 101', 'SEM', 'Fall', 'second', 2024, 60, 'TBA', 'TBA'),
('COMPSCI 101', 'LAB', 'Fall', 'second', 2024, 30, 'TBA', 'TBA'),
('COMPSCI 101', 'LAB', 'Fall', 'second', 2024, 30, 'TBA', 'TBA'),
('COMPSCI 201', 'SEM', 'Fall', 'first', 2024, 40, 'IB', '2071'),
('COMPSCI 201', 'LAB', 'Fall', 'first', 2024, 20, 'AB', '3101'),
('COMPSCI 201', 'LAB', 'Fall', 'first', 2024, 20, 'AB', '3101'),
('COMPSCI 201', 'SEM', 'Fall', 'second', 2024, 40, 'AB', '1087'),
('COMPSCI 201', 'REC', 'Fall', 'second', 2024, 40, 'AB', '1079'),
('COMPSCI 201', 'LAB', 'Fall', 'second', 2024, 20, 'AB', '3103'),
('COMPSCI 201', 'LAB', 'Fall', 'second', 2024, 20, 'AB', '3103'),
('COMPSCI 203', 'LEC', 'Fall', 'first', 2024, 40, 'AB', '1079'),
('COMPSCI 203', 'REC', 'Fall', 'first', 2024, 40, 'AB', '1079'),
('COMPSCI 205', 'SEM', 'Fall', 'second', 2024, 40, 'AB', '1079'),
('COMPSCI 205', 'REC', 'Fall', 'second', 2024, 40, 'AB', '1087'),
('COMPSCI 207', 'SEM', 'Fall', 'second', 2024, 40, 'AB', '3103'),
('COMPSCI 301', 'SEM', 'Fall', 'second', 2024, 40, 'WDR', '1100'),
('COMPSCI 301', 'REC', 'Fall', 'second', 2024, 40, 'WDR', '1100'),
('COMPSCI 308', 'SEM', 'Fall', 'second', 2024, 40, 'IB', '2050'),
('COMPSCI 309', 'SEM', 'Fall', 'first', 2024, 40, 'LIB', '1123'),
('COMPSCI 309', 'REC', 'Fall', 'first', 2024, 40, 'LIB', '1123'),
('COMPSCI 310', 'LEC', 'Fall', 'second', 2024, 32, 'CCT', 'E1011'),
('COMPSCI 402', 'SEM', 'Fall', 'first', 2024, 25, 'IB', '1011'),
('MATH 101', 'LEC', 'Fall', 'first', 2024, 40, 'AB', '1087'),
('MATH 101', 'REC', 'Fall', 'first', 2024, 40, 'AB', '1087'),
('MATH 105', 'LEC', 'Fall', 'first', 2024, 60, 'AB', '1087'),
('MATH 105', 'REC', 'Fall', 'first', 2024, 60, 'AB', '1087'),
('MATH 105', 'LEC', 'Fall', 'first', 2024, 60, 'AB', '2107'),
('MATH 105', 'REC', 'Fall', 'first', 2024, 60, 'AB', '2107'),
('MATH 105', 'LEC', 'Fall', 'second', 2024, 60, 'IB', '2071'),
('MATH 105', 'REC', 'Fall', 'second', 2024, 60, 'IB', '1047'),
('MATH 105', 'LEC', 'Fall', 'second', 2024, 60, 'IB', '1046'),
('MATH 105', 'REC', 'Fall', 'second', 2024, 60, 'IB', '1046'),
('MATH 201', 'SEM', 'Fall', 'first', 2024, 40, 'IB', '1046'),
('MATH 201', 'REC', 'Fall', 'first', 2024, 40, 'IB', '1046'),
('MATH 201', 'SEM', 'Fall', 'second', 2024, 40, 'IB', '1046'),
('MATH 201', 'REC', 'Fall', 'second', 2024, 40, 'IB', '1046'),
('MATH 202', 'SEM', 'Fall', 'first', 2024, 40, 'IB', '2028'),
('MATH 202', 'REC', 'Fall', 'first', 2024, 40, 'IB', '2028'),
('MATH 202', 'SEM', 'Fall', 'second', 2024, 40, 'AB', '2107'),
('MATH 202', 'REC', 'Fall', 'second', 2024, 40, 'AB', '2107'),
('MATH 203', 'LEC', 'Fall', 'second', 2024, 40, 'AB', '3103'),
('MATH 203', 'REC', 'Fall', 'second', 2024, 40, 'AB', '3103'),
('MATH 206', 'LEC', 'Fall', 'first', 2024, 40, 'IB', '1047'),
('MATH 206', 'REC', 'Fall', 'first', 2024, 40, 'IB', '1047'),
('MATH 206', 'LEC', 'Fall', 'second', 2024, 40, 'IB', '1046'),
('MATH 206', 'REC', 'Fall', 'second', 2024, 40, 'IB', '1046'),
('MATH 302', 'SEM', 'Fall', 'first', 2024, 25, 'LIB', '1119'),
('MATH 302', 'LAB', 'Fall', 'first', 2024, 25, 'LIB', '1119'),
('MATH 303', 'SEM', 'Fall', 'second', 2024, 25, 'WDR', '1007'),
('MATH 304', 'SEM', 'Fall', 'second', 2024, 25, 'WDR', '1003'),
('MATH 304', 'REC', 'Fall', 'second', 2024, 25, 'WDR', '1005'),
('MATH 305', 'SEM', 'Fall', 'first', 2024, 25, 'IB', '2025'),
('MATH 305', 'REC', 'Fall', 'first', 2024, 25, 'IB', '1056'),
('MATH 307', 'SEM', 'Fall', 'first', 2024, 25, 'IB', '1012'),
('MATH 308', 'SEM', 'Fall', 'second', 2024, 25, 'CCT', 'E2011'),
('MATH 407', 'LEC', 'Fall', 'second', 2024, 18, 'WDR', '1007'),
('MATH 408', 'SEM', 'Fall', 'first', 2024, 25, 'IB', '2001'),
('MATH 412', 'LEC', 'Fall', 'second', 2024, 25, 'IB', '1052'),
('MATH 450', 'SEM', 'Fall', 'second', 2024, 25, 'IB', '1017'),
('STATS 101', 'LEC', 'Fall','first', 2024, 32, 'IB', '3106'),
('STATS 101', 'LAB', 'Fall','first', 2024, 32, 'IB', '3106'),
('STATS 101', 'LEC', 'Fall','first', 2024, 32, 'IB', '3106'),
('STATS 101', 'LAB', 'Fall','first', 2024, 32, 'IB', '3106'),
('STATS 101', 'LEC', 'Fall','second', 2024, 32, 'AB', '3101'),
('STATS 101', 'LAB', 'Fall','second', 2024, 32, 'AB', '3101'),
('STATS 101', 'LEC', 'Fall','second', 2024, 32, 'IB', '3106'),
('STATS 101', 'LAB', 'Fall','second', 2024, 32, 'IB', '3106'),
('STATS 102', 'LEC', 'Fall', 'first', 2024, 60, 'IB', '2071'),
('STATS 102', 'LAB', 'Fall', 'first', 2024, 60, 'IB', '2071'),
('STATS 201', 'SEM', 'Fall', 'second', 2024, 18, 'LIB', '2113'),
('STATS 202', 'LEC', 'Fall', 'second', 2024, 60, 'IB', '2028'),
('STATS 202', 'LAB', 'Fall', 'second', 2024, 60, 'IB', '2071'),
('STATS 211', 'LEC', 'Fall', 'second', 2024, 40, 'AB', '1087'),
('STATS 211', 'REC', 'Fall', 'second', 2024, 40, 'AB', '1087'),
('STATS 302', 'SEM', 'Fall', 'first', 2024, 40, 'LIB', '1123'),
('STATS 302', 'REC', 'Fall', 'first', 2024, 40, 'LIB', '1123'),
('STATS 303', 'SEM', 'Fall', 'second', 2024, 40, 'LIB', '2115'),
('STATS 303', 'REC', 'Fall', 'second', 2024, 40, 'LIB', '2115'),
('STATS 401', 'SEM', 'Fall', 'first', 2024, 40, 'LIB', '1123'),
('STATS 402', 'SEM', 'Fall', 'second', 2024, 40, 'LIB', '2115');

insert into instructor_master (id, first_name, last_name, dept, salary, isDuke, is_active)
select id, first_name, last_name, dept, salary, isDuke, true
from instructor;

insert into instructor_master (id, first_name, last_name, dept, salary, isDuke, is_active)
select id, first_name, last_name, dept, salary, isDuke, false
from past_instructor;


insert into teaches (instructor_id, section_id) value 
('bl291', 1),
('bl291', 2),
('bl291', 3),
('dl288', 4),
('dl288', 5),
('dl288', 6),
('yg281', 5),
('yg281', 6),
('mm940', 7),
('mm940', 8),
('mm940', 9),
('ft47', 7),
('ft47', 8),
('ft47', 9),
('ft47', 10),
('ft47', 11),
('ft47', 12),
('ft47', 13),
('xc171', 14),
('xc171', 15),
('mh596', 16),
('mh596', 17),
('mh596', 18),
('js1242', 19),
('js1242', 20),
('xc171', 21),
('mm940', 22),
('mm940', 23),
('mm940', 24),
('ps298', 25),
('dc383', 26),
('dc383', 27),
('zh148', 28),
('zh148', 29),
('dz95', 30),
('dz95', 31),
('hh321', 32),
('hh321', 33),
('pg180', 34),
('pg180', 35),
('yg281', 35),
('is124', 36),
('is124', 37),
('is124', 38),
('is124', 39),
('pg180', 40),
('pg180', 41),
('dc383', 42),
('dc383', 43),
('sx59', 44),
('sx59', 45),
('pjg32', 46),
('pjg32', 47),
('is124', 48),
('is124', 49),
('ke83', 50),
('ke83', 51),
('pjg32', 52),
('ps298', 53),
('ps298', 54),
('sx59', 55),
('sx59', 56),
('lj176', 57),
('zh148', 58),
('mw170', 59),
('pjg32', 60),
('jl164', 61),
('jl164', 62),
('awm31', 63),
('awm31', 64),
('mn279', 65),
('mn279', 66),
('jy313', 67),
('jy313', 68),
('mn279', 69),
('mn279', 70),
('ml442', 71),
('ml442', 72),
('lz183', 73),
('pw160', 74),
('pw160', 75),
('cv127', 76),
('cv127', 77),
('mm940', 78),
('mm940', 79),
('dz95', 80),
('dz95', 81),
('yj232', 82),
('ps298', 83);

insert into course_req (course_id, req_id, type, group_id) values 
('COMPSCI 101', 'COMPSCI 201', 'antireq', 0),
('COMPSCI 101', 'STATS 102', 'antireq', 0),
('COMPSCI 203', 'COMPSCI 201', 'prereq', 0),
('COMPSCI 203', 'MATH 202', 'prereq', 1),
('COMPSCI 203', 'COMPSCI 201', 'coreq', 0),
('COMPSCI 203', 'MATH 202', 'coreq', 1),
('COMPSCI 205', 'COMPSCI 201', 'prereq', 0),
('COMPSCI 207', 'COMPSCI 101', 'prereq', 0),
('COMPSCI 207', 'COMPSCI 201', 'prereq', 1),
('COMPSCI 207', 'STATS 102', 'prereq', 2),
('COMPSCI 301', 'STATS 201', 'prereq', 0),
('COMPSCI 301', 'COMPSCI 308', 'antireq', 0),
('COMPSCI 301', 'COMPSCI 310', 'antireq', 0),
('COMPSCI 308', 'COMPSCI 201', 'prereq', 0),
('COMPSCI 308', 'COMPSCI 203', 'prereq', 0),
('COMPSCI 308', 'COMPSCI 201', 'prereq', 1),
('COMPSCI 308', 'MATH 205', 'prereq', 1),
('COMPSCI 308', 'COMPSCI 201', 'prereq', 2),
('COMPSCI 308', 'MATH 206', 'prereq', 2),
('COMPSCI 309', 'MATH 201', 'prereq', 0),
('COMPSCI 309', 'MATH 202', 'prereq', 0),
('COMPSCI 309', 'MATH 206', 'prereq', 0),
('COMPSCI 309', 'COMPSCI 201', 'prereq', 0),
('COMPSCI 309', 'STATS 302', 'antireq', 0),
('COMPSCI 309', 'MATH 405', 'antireq', 0),
('COMPSCI 310', 'COMPSCI 201', 'prereq', 0),
('COMPSCI 402', 'STATS 302', 'prereq', 0),
('COMPSCI 402', 'COMPSCI 309', 'prereq', 1),
('COMPSCI 402', 'MATH 405', 'prereq', 2),
('COMPSCI 402', 'COMPSCI 201', 'prereq', 2),
('MATH 202', 'MATH 101', 'prereq', 0),
('MATH 202', 'MATH 105', 'prereq', 1),
('MATH 203', 'MATH 101', 'prereq', 0),
('MATH 203', 'MATH 105', 'prereq', 1),
('MATH 205', 'MATH 101', 'prereq', 0),
('MATH 205', 'MATH 105', 'prereq', 1),
('MATH 205', 'MATH 206', 'antireq', 0),
('MATH 206', 'MATH 101', 'prereq', 0),
('MATH 206', 'MATH 105', 'prereq', 1),
('MATH 206', 'MATH 205', 'antireq', 0),
('MATH 302', 'MATH 201', 'prereq', 0),
('MATH 302', 'MATH 202', 'prereq', 0),
('MATH 302', 'COMPSCI 101', 'prereq', 0),
('MATH 302', 'MATH 201', 'prereq', 1),
('MATH 302', 'MATH 202', 'prereq', 1),
('MATH 302', 'COMPSCI 201', 'prereq', 1),
('MATH 302', 'MATH 201', 'prereq', 2),
('MATH 302', 'MATH 202', 'prereq', 2),
('MATH 302', 'STATS 102', 'prereq', 2),
('MATH 302', 'MATH 304', 'antireq', 0),
('MATH 303', 'MATH 201', 'prereq', 0),
('MATH 303', 'MATH 202', 'prereq', 0),
('MATH 304', 'MATH 201', 'prereq', 0),
('MATH 304', 'MATH 202', 'prereq', 0),
('MATH 304', 'COMPSCI 101', 'prereq', 0),
('MATH 304', 'MATH 201', 'prereq', 1),
('MATH 304', 'MATH 202', 'prereq', 1),
('MATH 304', 'COMPSCI 201', 'prereq', 1),
('MATH 304', 'MATH 201', 'prereq', 2),
('MATH 304', 'MATH 202', 'prereq', 2),
('MATH 304', 'STATS 102', 'prereq', 2),
('MATH 304', 'MATH 302', 'antireq', 0),
('MATH 305', 'MATH 201', 'prereq', 0),
('MATH 305', 'MATH 202', 'prereq', 0),
('MATH 307', 'MATH 201', 'prereq', 0),
('MATH 307', 'MATH 202', 'prereq', 0),
('MATH 308', 'MATH 203', 'prereq', 0),
('MATH 308', 'MATH 205', 'prereq', 0),
('MATH 308', 'STATS 211', 'prereq', 0),
('MATH 407', 'MATH 201', 'prereq', 0),
('MATH 407', 'MATH 202', 'prereq', 0),
('MATH 408', 'MATH 201', 'prereq', 0),
('MATH 408', 'MATH 202', 'prereq', 0),
('MATH 412', 'MATH 202', 'prereq', 0),
('MATH 412', 'MATH 308', 'prereq', 0),
('MATH 450', 'MATH 308', 'prereq', 0),
('STATS 102', 'COMPSCI 101', 'antireq', 0),
('STATS 201', 'MATH 101', 'prereq', 0),
('STATS 201', 'STATS 101', 'prereq', 0),
('STATS 201', 'MATH 105', 'prereq', 1),
('STATS 201', 'STATS 101', 'prereq', 1),
('STATS 201', 'MATH 205', 'prereq', 2),
('STATS 201', 'MATH 206', 'prereq', 3),
('STATS 202', 'STATS 101', 'prereq', 0),
('STATS 202', 'MATH 205', 'prereq', 1),
('STATS 202', 'MATH 206', 'prereq', 2),
('STATS 202', 'COMPSCI 309', 'antireq', 0),
('STATS 202', 'STATS 302', 'antireq', 0),
('STATS 202', 'MATH 405', 'antireq', 0),
('STATS 211', 'MATH 206', 'prereq', 0),
('STATS 211', 'STATS 210', 'antireq', 0),
('STATS 302', 'MATH 201', 'prereq', 0),
('STATS 302', 'MATH 202', 'prereq', 0),
('STATS 302', 'MATH 206', 'prereq', 0),
('STATS 302', 'COMPSCI 201', 'prereq', 0),
('STATS 302', 'COMPSCI 309', 'antireq', 0),
('STATS 302', 'MATH 405', 'antireq', 0),
('STATS 303', 'STATS 302', 'prereq', 0),
('STATS 303', 'STATS 211', 'prereq', 0),
('STATS 303', 'MATH 304', 'prereq', 0),
('STATS 303', 'MATH 305', 'prereq', 0),
('STATS 303', 'STATS 302', 'coreq', 0),
('STATS 303', 'STATS 211', 'coreq', 0),
('STATS 303', 'MATH 304', 'coreq', 0),
('STATS 303', 'MATH 305', 'coreq', 0),
('STATS 303', 'MATH 405', 'prereq', 1),
('STATS 303', 'COMPSCI 201', 'prereq', 1),
('STATS 303', 'STATS 211', 'prereq', 1),
('STATS 303', 'MATH 304', 'prereq', 1),
('STATS 303', 'MATH 305', 'prereq', 1),
('STATS 303', 'MATH 405', 'coreq', 1),
('STATS 303', 'COMPSCI 201', 'coreq', 1),
('STATS 303', 'STATS 211', 'coreq', 1),
('STATS 303', 'MATH 304', 'coreq', 1),
('STATS 303', 'MATH 305', 'coreq', 1),
('STATS 401', 'MATH 206', 'prereq', 0),
('STATS 401', 'COMPSCI 201', 'prereq', 0),
('STATS 402', 'COMPSCI 309', 'prereq', 0),
('STATS 402', 'STATS 302', 'prereq', 1),
('STATS 402', 'MATH 405', 'prereq', 2),
('STATS 402', 'COMPSCI 201', 'prereq', 2);


insert into time_slot (start_time, end_time) values
('08:30:00', '09:45:00'),
('08:30:00', '11:00:00'),
('10:00:00', '11:15:00'),
('11:45:00', '13:00:00'),
('12:00:00', '14:30:00'),
('13:15:00', '14:30:00'),
('14:45:00', '16:00:00'),
('14:45:00', '17:15:00'),
('16:15:00', '17:30:00'),
('18:00:00', '19:15:00'),
('19:15:00', '20:15:00'),
('20:30:00', '22:00:00');


insert into section_time (section_id, time_slot_id, day) values 
(1, 4, 'Mon'),
(1, 4, 'Tue'),
(1, 4, 'Wed'),
(1, 4, 'Thu'),
(2, 9, 'Tue'),
(3, 7, 'Wed'),
(4, 6, 'Mon'),
(4, 6, 'Tue'),
(4, 6, 'Wed'),
(4, 6, 'Thu'),
(5, 7, 'Thu'),
(6, 9, 'Thu'),
(7, 3, 'Mon'),
(7, 3, 'Tue'),
(7, 3, 'Wed'),
(7, 3, 'Thu'),
(8, 9, 'Thu'),
(9, 7, 'Thu'),
(10, 5, 'Mon'),
(10, 5, 'Wed'),
(11, 7, 'Thu'),
(12, 9, 'Tue'),
(13, 9, 'Thu'),
(14, 1, 'Mon'),
(14, 1, 'Tue'),
(14, 1, 'Wed'),
(14, 1, 'Thu'),
(15, 10, 'Mon'),
(16, 3, 'Mon'),
(16, 3, 'Tue'),
(16, 3, 'Wed'),
(16, 3, 'Thu'),
(17, 7, 'Thu'),
(18, 4, 'Mon'),
(18, 4, 'Tue'),
(18, 4, 'Wed'),
(18, 4, 'Thu'),
(19, 5, 'Mon'),
(19, 5, 'Wed'),
(20, 6, 'Thu'),
(21, 6, 'Mon'),
(21, 6, 'Tue'),
(21, 6, 'Wed'),
(21, 6, 'Thu'),
(22, 1, 'Mon'),
(22, 1, 'Tue'),
(22, 1, 'Wed'),
(22, 1, 'Thu'),
(23, 6, 'Tue'),
(24, 9, 'Mon'),
(24, 9, 'Tue'),
(24, 9, 'Wed'),
(24, 9, 'Thu'),
(25, 5, 'Tue'),
(25, 5, 'Thu'),
(26, 6, 'Mon'),
(26, 6, 'Tue'),
(26, 6, 'Wed'),
(26, 6, 'Thu'),
(27, 7, 'Thu'),
(28, 3, 'Mon'),
(28, 3, 'Tue'),
(28, 3, 'Wed'),
(28, 3, 'Thu'),
(29, 4, 'Thu'),
(30, 7, 'Mon'),
(30, 7, 'Tue'),
(30, 7, 'Wed'),
(30, 7, 'Thu'),
(31, 9, 'Thu'),
(32, 1, 'Mon'),
(32, 1, 'Tue'),
(32, 1, 'Wed'),
(32, 1, 'Thu'),
(33, 3, 'Tue'),
(34, 6, 'Mon'),
(34, 6, 'Tue'),
(34, 6, 'Wed'),
(34, 6, 'Thu'),
(35, 7, 'Wed'),
(36, 1, 'Mon'),
(36, 1, 'Tue'),
(36, 1, 'Wed'),
(36, 1, 'Thu'),
(37, 9, 'Thu'),
(38, 3, 'Mon'),
(38, 3, 'Tue'),
(38, 3, 'Wed'),
(38, 3, 'Thu'),
(39, 7, 'Tue'),
(40, 3, 'Mon'),
(40, 3, 'Tue'),
(40, 3, 'Wed'),
(40, 3, 'Thu'),
(41, 7, 'Mon'),
(42, 6, 'Mon'),
(42, 6, 'Tue'),
(42, 6, 'Wed'),
(42, 6, 'Thu'),
(43, 7, 'Wed'),
(44, 6, 'Mon'),
(44, 6, 'Tue'),
(44, 6, 'Wed'),
(44, 6, 'Thu'),
(45, 7, 'Wed'),
(46, 6, 'Mon'),
(46, 6, 'Tue'),
(46, 6, 'Wed'),
(46, 6, 'Thu'),
(47, 7, 'Thu'),
(48, 4, 'Mon'),
(48, 4, 'Tue'),
(48, 4, 'Wed'),
(48, 4, 'Thu'),
(49, 7, 'Thu'),
(50, 5, 'Tue'),
(51, 5, 'Thu'),
(52, 10, 'Thu'),
(53, 7, 'Tue'),
(53, 7, 'Thu'),
(54, 10, 'Wed'),
(55, 8, 'Mon'),
(55, 8, 'Wed'),
(56, 7, 'Thu'),
(57, 12, 'Mon'),
(57, 12, 'Wed'),
(58, 9, 'Mon'),
(58, 9, 'Tue'),
(58, 9, 'Wed'),
(58, 9, 'Thu'),
(59, 5, 'Mon'),
(59, 5, 'Wed'),
(60, 1, 'Tue'),
(60, 1, 'Thu'),
(61, 1, 'Tue'),
(61, 1, 'Thu'),
(62, 5, 'Tue'),
(62, 5, 'Thu'),
(63, 1, 'Tue'),
(63, 1, 'Thu'),
(64, 6, 'Wed'),
(65, 8, 'Mon'),
(65, 8, 'Wed'),
(66, 4, 'Tue'),
(67, 5, 'Tue'),
(67, 5, 'Thu'),
(68, 7, 'Wed'),
(69, 8, 'Mon'),
(69, 8, 'Wed'),
(70, 7, 'Thu'),
(71, 6, 'Mon'),
(71, 6, 'Tue'),
(71, 6, 'Wed'),
(71, 6, 'Thu'),
(72, 7, 'Thu'),
(73, 1, 'Tue'),
(73, 1, 'Thu'),
(74, 5, 'Mon'),
(74, 5, 'Wed'),
(75, 10, 'Wed'),
(76, 3, 'Mon'),
(76, 3, 'Tue'),
(76, 3, 'Wed'),
(76, 3, 'Thu'),
(77, 11, 'Thu'),
(78, 1, 'Mon'),
(78, 1, 'Tue'),
(78, 1, 'Wed'),
(78, 1, 'Thu'),
(79, 6, 'Tue'),
(80, 1, 'Tue'),
(80, 1, 'Thu'),
(81, 4, 'Thu'),
(82, 5, 'Mon'),
(82, 5, 'Wed'),
(83, 8, 'Mon'),
(83, 8, 'Wed');


insert into section (course_id, type, term, session, year, capacity, building_name, room_name)
select course_id, type, 'spring', session, 2024, capacity, building_name, room_name
from section
where term = 'fall' and year = 2024;

insert into section (course_id, type, term, session, year, capacity, building_name, room_name)
select course_id, type, 'fall', session, 2023, capacity, building_name, room_name
from section
where term = 'fall' and year = 2024;

insert into section (course_id, type, term, session, year, capacity, building_name, room_name)
select course_id, type, 'spring', session, 2023, capacity, building_name, room_name
from section
where term = 'fall' and year = 2024;

insert into section (course_id, type, term, session, year, capacity, building_name, room_name)
select course_id, type, 'fall', session, 2022, capacity, building_name, room_name
from section
where term = 'fall' and year = 2024;

insert into section (course_id, type, term, session, year, capacity, building_name, room_name)
select course_id, type, 'spring', session, 2022, capacity, building_name, room_name
from section
where term = 'fall' and year = 2024;

insert into section (course_id, type, term, session, year, capacity, building_name, room_name)
select course_id, type, 'fall', session, 2021, capacity, building_name, room_name
from section
where term = 'fall' and year = 2024;

insert into section (course_id, type, term, session, year, capacity, building_name, room_name)
select course_id, type, 'spring', session, 2021, capacity, building_name, room_name
from section
where term = 'fall' and year = 2024;

SET SQL_SAFE_UPDATES = 0;
alter table section add column new_id int;
set @new_id = 0;
update section set id = (@new_id := @new_id + 1) where id is not null;
alter table section drop column new_id;
SET SQL_SAFE_UPDATES = 1;


drop procedure if exists insert_multiple_rows;
delimiter $$
create procedure insert_multiple_rows()
begin
    declare counter int default 1;
    declare max_iterations int default 7;

    while counter <= max_iterations do
        insert into section_time (section_id, time_slot_id, day)
        select 
            section_id + (select max(section_id) from section_time), 
            time_slot_id, 
            day
        from section_time
        where section_id <= 83;

        insert into teaches (instructor_id, section_id)
        select 
            instructor_id,
            section_id + (select max(section_id) from teaches)
        from teaches
        where section_id <= 83;
        set counter = counter + 1;
    end while;
end$$

delimiter ;
call insert_multiple_rows();



insert into credit_limit(student_id, year, term, session, credit_limit) values 
('yg202', 2024, 'Fall', 'first', 21),
('yg202', 2024, 'Fall', 'second', 21),
('yg202', 2024, 'Spring', 'first', 21),
('yg202', 2024, 'Spring', 'second', 21),
('yg202', 2023, 'Fall', 'first', 21),
('yg202', 2023, 'Fall', 'second', 21),
('yg202', 2023, 'Spring', 'first', 21),
('yg202', 2023, 'Spring', 'second', 21),
('jc923', 2024, 'Fall', 'first', 21),
('jc923', 2024, 'Fall', 'second', 21),
('jc923', 2024, 'Spring', 'first', 21),
('jc923', 2024, 'Spring', 'second', 21),
('jc923', 2023, 'Fall', 'first', 21),
('jc923', 2023, 'Fall', 'second', 21),
('jc923', 2023, 'Spring', 'first', 21),
('jc923', 2023, 'Spring', 'second', 21),
('jq48', 2024, 'Fall', 'first', 21),
('jq48', 2024, 'Fall', 'second', 21),
('jq48', 2024, 'Spring', 'first', 21),
('jq48', 2024, 'Spring', 'second', 21),
('jq48', 2023, 'Fall', 'first', 21),
('jq48', 2023, 'Fall', 'second', 21),
('jq48', 2023, 'Spring', 'first', 21),
('jq48', 2023, 'Spring', 'second', 21);



insert into course_division (course_id, division)
select distinct(id), 'Natural Science'
from course;

insert into address (student_id, type, country, province, city, zip_code, street, street_number, unit)
select 
    id as student_id,
    'mail' as type,
    'United States' as country,
    'North Carolina' as province,
    'Durham' as city,
    '27708' as zip_code,
    'Campus Drive' as street,
    '123' as street_number,
    null as unit
from student;

insert into phone_number (student_id, type, country_code, area_code, number)
values ('yg202', 'work', 86, 0, '13665325649');


insert into enrollment (student_id, section_id, grade) values 
('yg202', 403, 'C'), -- STAT2 102. Fall 2022 
('yg202', 404, 'C'), 
('yg202', 360, 'B'), -- MATH 105
('yg202', 361, 'B'), 
('yg202', 374, 'B'), -- MATH 202
('yg202', 375, 'B'), 
('yg202', 342, 'D'), -- CS 201
('yg202', 343, 'D'), 
('yg202', 344, 'D'), 
('yg202', 285, 'C'), -- MATH 201. Spring 2023
('yg202', 286, 'C'), 
('yg202', 295, 'B'), -- MATH 206
('yg202', 296, 'B'), 
('yg202', 265, 'B'), -- CS 205
('yg202', 266, 'B'), 
('yg202', 267, 'D'), -- CS 207
('yg202', 216, 'C'), -- MATH 302. Fall 2023
('yg202', 217, 'C'), 
('yg202', 180, 'B'), -- CS 203
('yg202', 181, 'B'), 
('yg202', 210, 'B'), -- MATH 203
('yg202', 211, 'B'), 
('yg202', 218, 'D'), -- MATH 303
('yg202', 105, 'C'), -- CS 309. Spring 2024
('yg202', 106, 'C'), 
('yg202', 165, 'B'), -- STATS 401
('yg202', 104, 'B'), -- CS 308
('yg202', 141, 'D'); -- MATH 308

insert into shopping (student_id, section_id) values 
('yg202', 55), -- MATH 305. Fall 2024
('yg202', 56), 
('yg202', 57), -- MATH 307
('yg202', 24), -- CS 310
('yg202', 80), -- STATS 303 cannot enroll
('yg202', 81);

insert into enrollment (student_id, section_id, grade) values 
('jc923', 167, 'A'), -- CS 101. Fall 2023
('jc923', 168, 'A'),
('jc923', 192, 'A'), -- MATH 105
('jc923', 193, 'A'),
('jc923', 176, 'A'), -- CS 201
('jc923', 177, 'A'), 
('jc923', 208, 'A'), -- MATH 202
('jc923', 209, 'A'), 
('jc923', 119, 'A'), -- MATH 201. Spring 2024
('jc923', 120, 'A'),
('jc923', 129, 'A'), -- MATH 206
('jc923', 130, 'A'),
('jc923', 99, 'A'), -- CS 205
('jc923', 100, 'A'),
('jc923', 101, 'A'); -- CS 207


insert into shopping (student_id, section_id) values 
('jc923', 22), -- CS 309. Fall 2024
('jc923', 23), 
('jc923', 57), -- MATH 307
('jc923', 24), -- CS 310
('jc923', 80), -- STATS 303 cannot enroll
('jc923', 81);


insert into enrollment (student_id, section_id, grade) values 
('jq48', 237, 'A'), -- STATS 102. Fall 2023
('jq48', 238, 'A'),
('jq48', 194, 'A'), -- MATH 105
('jq48', 195, 'A'),
('jq48', 204, 'A'), -- MATH 201
('jq48', 205, 'A'),
('jq48', 210, 'A'), -- MATH 203
('jq48', 211, 'A'),
('jq48', 90, 'A'), -- CS 201. Spring 2023
('jq48', 91, 'A'),
('jq48', 123, 'A'), -- MATH 202
('jq48', 124, 'A'),
('jq48', 99, 'A'), -- CS 205
('jq48', 100, 'A'),
('jq48', 104, 'A'); -- CS 308

insert into shopping (student_id, section_id) values 
('jq48', 22), -- CS 309. Fall 2024
('jq48', 23), 
('jq48', 57), -- MATH 307
('jq48', 24), -- CS 310
('jq48', 18); -- CS 207

insert into admin values ('admin');

insert into login_info(id, password, type) values 
('yg202', 123456, 'student'),
('jc923', 123456, 'student'),
('jq48', 123456, 'student'),
('admin', 123456, 'admin'),
('mm940', 123456, 'instructor');

insert into balance (student_id, due, paid)
values ('yg202', 100000, 100000);
