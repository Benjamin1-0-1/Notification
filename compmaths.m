% Vector operations demo
r = [2,3,4];
r1 = [2,6,3];
c = [2;3;4];
c1 = [7;2;9];

% Basic operations
V = r + c.'; % align column to row before addition
v1 = r + r1;
b = c - c1;
disp('V = r + c'' ->'); disp(V);
disp('v1 = r + r1 ->'); disp(v1);
disp('b = c - c1 ->'); disp(b);

% Scalar multiplication
p = pi;
m = p * r;
disp('m = pi * r ->'); disp(m);

% Transpose
t = r';
disp('transpose of r ->'); disp(t);

% Dot product
s = dot(r, r1);
disp('dot product of r and r1 ->'); disp(s);

% Magnitude
q = sqrt(dot(r, r));
disp('magnitude of r ->'); disp(q);

% Cross product
j = cross(c, c1);
disp('cross product of c and c1 ->'); disp(j);

% Triangle area via cross of edge vectors
A = [2,3,4];
B = [4,8,10];
C = [15,11,17];
o = C - A;
l = B - A;
d = cross(o, l);
area = 0.5 * sqrt(dot(d, d));
disp('triangle area from A,B,C ->');
disp(area);

%MATRICES
M = [2,3,4;
    5,6,7;
    8,9,10
    ];
B = [1,2,3;
     4,5,6;
     7,8,9
    ];
disp('Matrix M ->'); disp(M);
disp('Matrix B ->'); disp(B);
%Basic matrix operations
% addition
S = M + B;
disp('Matrix S = M + B ->'); disp(S);
% subtraction
D = M - 2*B;
disp('Matrix D = M - 2*B ->'); disp(D);
%Determinant and inverse operations
detM = det(M);
invM = inv(M);
disp('Determinant of M ->'); disp(detM);
disp('Inverse of M ->'); disp(invM);
%validate answer
validate = M * invM;
disp('Validation of inverse ->'); disp(validate);
%Selecting single elements in a matrix
elem = M(3,2); % element at row 3, column 2
disp('Element at row 3, column 2 of M ->'); disp(elem);
m_1c= M(1,:); % first row, all columns
disp('First row of M ->'); disp(m_1c);
m_11= M(2:3 ,2:3); % all rows, first column
disp('minor ofpr 1-1 is ->'); disp(m_11);
disp('the actual value of the minor is ->'); disp(det(m_11));
m_r3 = M(:,3); % all rows, third column
disp('Third column of M ->'); disp(m_r3);
%trace
traceM = trace(M);
disp('Trace of M ->'); disp(traceM);
%rank
rankM = rank(M);
disp('Rank of M ->'); disp(rankM);
