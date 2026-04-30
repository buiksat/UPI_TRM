set datafile separator '\t'
set xlabel 'Evaluator depth n'
set ylabel 'Value error / certificate'
set title 'Finite-MDP value-error decomposition'
set key outside
set grid
set logscale y
set terminal pdfcairo enhanced color size 6.2in,3.8in font ',10'
set output '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_validation/fig_value_decomposition.pdf'
plot '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_validation/fig_value_decomposition.dat' using 1:2 with lines lc rgb '#1b9e77' lw 2 title 'L_z=0.20 error', \
+    '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_validation/fig_value_decomposition.dat' using 1:3 with lines dt 2 lc rgb '#1b9e77' lw 2 title 'L_z=0.20 bound', \
+    '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_validation/fig_value_decomposition.dat' using 1:4 with lines lc rgb '#d95f02' lw 2 title 'L_z=0.50 error', \
+    '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_validation/fig_value_decomposition.dat' using 1:5 with lines dt 2 lc rgb '#d95f02' lw 2 title 'L_z=0.50 bound', \
+    '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_validation/fig_value_decomposition.dat' using 1:6 with lines lc rgb '#7570b3' lw 2 title 'L_z=0.80 error', \
+    '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_validation/fig_value_decomposition.dat' using 1:7 with lines dt 2 lc rgb '#7570b3' lw 2 title 'L_z=0.80 bound', \
+    '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_validation/fig_value_decomposition.dat' using 1:8 with lines lc rgb '#e7298a' lw 2 title 'L_z=0.95 error', \
+    '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_validation/fig_value_decomposition.dat' using 1:9 with lines dt 2 lc rgb '#e7298a' lw 2 title 'L_z=0.95 bound'
set terminal pngcairo size 1600,980 enhanced font ',10'
set output '/home/buiksat/UPI_TRM/UPI_TRM_NIPS/results/episodic_z_validation/fig_value_decomposition.png'
replot
