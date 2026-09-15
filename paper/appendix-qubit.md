# Appendix A. A decoder fixed by two oblique qubit effects

This appendix proves Theorem 6.1 of the main manuscript. All tensor identities
on Stinespring environments are suppressed when no confusion is possible.
No result in this appendix assumes access to that environment.

## A.1. Fix the decoder before choosing a channel

Discard scalar logical reflections. Write each remaining one as
\(R_y=n_y\cdot\sigma\). The finite irreducible family has a pair maximizing
\(s=|n_1\times n_2|>0\). A fixed logical unitary and orientation put this
pair in the form

\[
R_1=Z,\qquad R_2=cZ+sX,\qquad c^2+s^2=1.
\tag{A.1}
\]

For the two fixed physical effects put \(C_i=2Q_i-I\), and form the
Halmos reflection dilations on \(\mathbb C^{2m}\):

\[
A=\begin{pmatrix}C_1&\sqrt{I-C_1^2}\\
\sqrt{I-C_1^2}&-C_1\end{pmatrix},\qquad
B=\begin{pmatrix}C_2&\sqrt{I-C_2^2}\\
\sqrt{I-C_2^2}&-C_2\end{pmatrix}.
\tag{A.2}
\]

Both square to identity. Double once more:
\(A'=A\oplus(-A)\), \(B'=B\oplus(-B)\), and
\(H'=(A'B'-B'A')/(2i)=H\oplus H\). Since
\(A'H'A'=-H'\), the first reflection exchanges the positive and negative
spectral spaces of \(H'\). On the nonzero spectrum choose the usual sign.
On the remaining space \(\ker H\oplus\ker H\), choose instead the
copy-exchange map \((\xi,\zeta)\mapsto(\zeta,\xi)\). The resulting
operator \(S\) obeys

\[
S=S^*,\quad S^2=I,\quad A'S=-SA',\quad H'=S|H'|.
\tag{A.3}
\]

The exchange rule is essential: arbitrary independent signs on zero modes
need not anticommute with \(A'\).

Two anticommuting reflections give an exact qubit representation. More
explicitly, \(S\) maps the positive eigenspace of \(A'\) isometrically
onto the negative one, so their dimensions agree. Choose bases related by
this map and adjust a phase. This produces a unitary
\(W:\mathbb C^{4m}\to\mathbb C^2\otimes\mathbb C^{2m}\) satisfying

\[
WA'W^*=Z\otimes I,\quad WSW^*=Y\otimes I,\quad
W(iA'S)W^*=X\otimes I.
\tag{A.4}
\]

Let \(J:\mathbb C^m\to\mathbb C^{4m}\) embed into the first copy, and
define

\[
D_{R,Q}(\rho)=\operatorname{Tr}_{2m}(WJ\rho J^*W^*).
\tag{A.5}
\]

Transform back by the fixed logical coordinate choice when necessary. This
is CPTP and depends only on the logical family and its fixed physical effects.
It has been defined before any noise channel, error parameter or Stinespring
representation is chosen.

## A.2. First and second moments under a compatible pullback

Now fix an arbitrary compatible \(E\). Let \(V\) be its Stinespring
isometry followed by \(J\), and write \(\phi(T)=V^*(T\otimes I)V\).
Then \(\phi\) is UCP and

\[
a=\phi(A'),\quad b=\phi(B'),\qquad
\|a-Z\|,\ \|b-(cZ+sX)\|\le2e.
\tag{A.6}
\]

For UCP maps the standard CP Schwarz/covariance estimate [C74] gives

\[
\|\phi(XY)-\phi(X)\phi(Y)\|
\le\|\phi(XX^*)-\phi(X)\phi(X)^*\|^{1/2}
\|\phi(Y^*Y)-\phi(Y)^*\phi(Y)\|^{1/2}.
\tag{A.7}
\]

Indeed insert \(I-VV^*\) between \(X,Y\) and use the two factor norms.
Since \(A',B'\) are reflections, their left and right defects coincide,
and \(\|I-a^2\|,\|I-b^2\|\le4e\).

Put \(U=A'B'\) and \(U_0=Z(cZ+sX)=cI+isY\). Equation (A.7) and
the two calibration errors yield \(\|\phi(U)-U_0\|\le8e\). Both
unitary defects of \(u=\phi(U)\) are at most \(16e\). Applying (A.7)
to \(U^2\), then comparing \(u^2\) with \(U_0^2\), gives

\[
\|\phi(U^2)-U_0^2\|\le32e,
\quad \|\phi(U^{*2})-U_0^{*2}\|\le32e.
\tag{A.8}
\]

As \(H'=(U-U^*)/(2i)\) and \(H'^2=(2I-U^2-U^{*2})/4\),

\[
\|h-sY\|\le8e,\qquad
\|k-s^2I\|\le16e,
\quad h=\phi(H'),\ k=\phi(H'^2).
\tag{A.9}
\]

Consequently

\[
\|H'V-sVY\|^2
=\|k-shY-sYh+s^2I\|\le32e=:q.
\tag{A.10}
\]

The completed sign \(S\) commutes with \(|H'|\) and preserves its kernel.
These estimates do not assume invertibility or a gap in the physical
commutator spectrum. The logical separation \(s>0\) is the only gap used.

## A.3. Sign rounding at linear error

Let \(\Pi_\pm=(I\pm S)/2\), \(G=|H'|\), and let
\(v_\pm=V|y_\pm\rangle\), where \(Y|y_\pm\rangle=\pm|y_\pm\rangle\).
On the wrong sign sector,
\((H'-s)\Pi_-v_+=-(G+s)\Pi_-v_+\). Thus (A.10) gives

\[
\|\Pi_-v_+\|^2,\quad\|\Pi_+v_-\|^2\le q/s^2.
\tag{A.11}
\]

This also handles the kernel, where the separation from the logical target
eigenvalue is exactly \(s\). The two diagonal entries of \(\phi(S)-Y\)
have modulus at most \(2q/s^2=64e/s^2\).

For its off-diagonal entry \(t=\langle v_+,Sv_-\rangle\), use

\[
\begin{aligned}
\langle v_+,H'v_-\rangle-st
={}&\langle\Pi_+v_+,(G-s)\Pi_+v_-\rangle\\
&-\langle\Pi_-v_+,(G-s)\Pi_-v_-\rangle.
\end{aligned}
\tag{A.12}
\]

In the first term, move the self-adjoint \(G-s\) onto \(\Pi_+v_+\),
whose residual norm is at most \(\sqrt q\); its other factor has norm
at most \(\sqrt q/s\). In the second term the residual acts on
\(\Pi_-v_-\), again a proper-sign factor of norm at most \(\sqrt q\),
and the remaining wrong-sign factor costs \(\sqrt q/s\). Thus the
right side of (A.12) has modulus at most \(2q/s\). Equation (A.9) also
gives \(|\langle v_+,H'v_-\rangle|\le8e\). Therefore

\[
|t|\le8e/s+2q/s^2\le72e/s^2.
\tag{A.13}
\]

Row-sum bounding the resulting Hermitian two-by-two matrix yields
\(\|\phi(S)-Y\|\le136e/s^2\).
For \(g=\phi(S)\), \(\|I-g^2\|\le272e/s^2\). Applying (A.7) to
\(A'S\) bounds its covariance by
\(\sqrt{4e\cdot272e/s^2}<33e/s\). Since \(iZY=X\),

\[
\|\phi(iA'S)-X\|\le2e+136e/s^2+33e/s\le171e/s^2.
\tag{A.14}
\]

All three recovered Pauli errors are thus at most \(171e/s^2\).

## A.4. Complete norm and geometry

For every amplification, write
\(T=I\otimes T_0+X\otimes T_x+Y\otimes T_y+Z\otimes T_z\).
Each coefficient is obtained by applying the norm-one functional
\(A\mapsto\tau_2(\sigma_jA)\) on the first factor; its completely
bounded norm is one. Hence \(\|T_j\|\le\|T\|\). The adjoint of
\(D_{R,Q}E-\mathrm{id}\) vanishes on \(I\), so

\[
\|D_{R,Q}E-\mathrm{id}\|_\diamond
=\|(D_{R,Q}E-\mathrm{id})^*\|_{\rm cb}
\le3\cdot171e/s^2.
\tag{A.15}
\]

The half-diamond bound is below \(257e/s^2\). If \(R_i\) is one member
of the selected maximizing pair, then
\(\|R_i-\tau_2(R_i)I\|=1\) and
\(\max_y\|[R_i,R_y]\|\le2s\). Therefore
\(\Gamma_{\rm cb}(R)\ge1/(2s)\), giving (6.1).

For each compatible \(E\), the proof chooses a possibly different
Stinespring witness but never changes (A.5). Thus the same decoder works
uniformly without a convexity assumption on the compatible family. The cap
by one treats all larger-error cases. Finiteness of the logical question
family ensures the maximizing pair exists.

## A.5. Resources and scope

The construction embeds the physical output of dimension \(m\) into
dimension \(4m\), equivalent to adding two clean qubits, applies a fixed
unitary identification and discards the multiplicity of dimension \(2m\).
There is no postselection, environmental access, extra channel use, or
channel-dependent correction. Exact square roots, a spectral sign, a kernel
split and the unitary identification are mathematical preprocessing. No
polynomial-time synthesis claim follows from their existence.
