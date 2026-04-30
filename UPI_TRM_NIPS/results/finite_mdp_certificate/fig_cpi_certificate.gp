set datafile separator '\t'
set xlabel 'Mixture weight alpha'
set ylabel 'Positive surrogate gap / certificate'
set title 'Finite-MDP CPI certificate (log scale)'
set key top left
set grid
set xrange [0.05:1.0]
set logscale y
set terminal pdfcairo enhanced color size 6.2in,3.8in font ',10'
set output '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/finite_mdp_certificate/fig_cpi_certificate.pdf'
plot '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/finite_mdp_certificate/fig_cpi_certificate.dat' using 1:2 with linespoints lw 2 pt 7 lc rgb '#0f4c81' title 'Lhat - eta',      '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/finite_mdp_certificate/fig_cpi_certificate.dat' using 1:3 with linespoints lw 2 pt 5 dt 2 lc rgb '#c0392b' title 'decomposition penalty',      '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/finite_mdp_certificate/fig_cpi_certificate.dat' using 1:4 with linespoints lw 2 pt 9 dt 3 lc rgb '#2d8659' title 'exact A penalty'
set terminal pngcairo size 1600,980 enhanced font ',10'
set output '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/finite_mdp_certificate/fig_cpi_certificate.png'
replot
