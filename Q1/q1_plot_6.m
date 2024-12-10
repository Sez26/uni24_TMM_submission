% visualising gravity model fitting
% Create a tiled layout for a 2x2 grid
t = tiledlayout(2, 2, 'TileSpacing', 'Compact', 'Padding', 'Compact');

% Title for the entire layout
title(t, 'UTLA Gravity Model', 'FontSize', 14, 'FontWeight', 'bold');

% First subplot
ax1 = nexttile;
% for MSOA plotting scatter every 100 values
smp_int = 1;
scatter(UTLA_x(1:smp_int:end), UTLA_y(1:smp_int:end), 'DisplayName', 'UTLA data')
hold on
% plotting fitted model
lin_lab = sprintf("Linear model: alpha = %.2f, c = %.2e.", UTLA_alpha, UTLA_c);
plot(UTLA_x, UTLA_fit.Fitted,'r-', 'LineWidth', 2, 'DisplayName', lin_lab)
title(ax1, 'Fitting Linear Model', 'Interpreter','latex');
xlabel(ax1, '$\log(d_{ij})$', 'Interpreter','latex');
ylabel(ax1, '$\log((T_{ij})/(O_i D_j))$', 'Interpreter','latex');
legend;
grid(ax1, 'on');

% residuals
ax2 = nexttile;
scatter(ax2, 1:smp_int:numel(UTLA_res), UTLA_res(1:smp_int:end));
hold on
scatter(ax2, 1:smp_int:numel(UTLA_res_OC), UTLA_res_OC(1:smp_int:end));
scatter(ax2, 1:smp_int:numel(UTLA_res_DC), UTLA_res_DC(1:smp_int:end));
title(ax2, 'Residuals', 'Interpreter','latex');
xlabel(ax2, 'Indices', 'Interpreter','latex');
ylabel(ax2, 'Residuals', 'Interpreter','latex');
legend(["Unconstrained","Origin Contrained","Destination Constrained"])
grid(ax2, 'on');

% exclude diagonals
% Get the size of the matrix
[m, n] = size(UTLA_res);
% Create a logical mask for the diagonal elements
diagMask = eye(m, n);
% Create a logical mask for all elements (complement of the diagonal)
nonDiagMask = ~diagMask;
lin_non_diag_idx = find(nonDiagMask);
ax3 = nexttile;
scatter(ax3, lin_non_diag_idx(1:smp_int:end), UTLA_res(lin_non_diag_idx(1:smp_int:end)));
hold on
scatter(ax3, lin_non_diag_idx(1:smp_int:end), UTLA_res_OC(lin_non_diag_idx(1:smp_int:end)));
scatter(ax3, lin_non_diag_idx(1:smp_int:end), UTLA_res_DC(lin_non_diag_idx(1:smp_int:end)));
title(ax3, 'Residuals - No Domestic Journeys', 'Interpreter','latex');
xlabel(ax3, 'Indices', 'Interpreter','latex');
ylabel(ax3, 'Residuals', 'Interpreter','latex');
legend(["Unconstrained","Origin Contrained","Destination Constrained"])
grid(ax3, 'on');

% Fourth subplot
ax4 = nexttile;
UTLA_y_OC = log(UTLA_OC(non_diag_idx)./(data.UTLAdata.O_tot(i).*data.UTLAdata.D_tot(j)));
hold on
UTLA_y_DC = log(UTLA_DC(non_diag_idx)./(data.UTLAdata.O_tot(i).*data.UTLAdata.D_tot(j)));
scatter(UTLA_x(1:smp_int:end), UTLA_y_OC, 'DisplayName', 'Origin Constrained')
scatter(UTLA_x(1:smp_int:end), UTLA_y(1:smp_int:end), 'DisplayName', 'Destination Contrained')
plot(UTLA_x, UTLA_fit.Fitted,'r-', 'LineWidth', 2, 'DisplayName', lin_lab)
title(ax4, 'Spread Comparison', 'interpreter', 'latex');
xlabel(ax4, 'X-axis');
ylabel(ax4, 'Y-axis');
legend(["Origin Constrained","Destination Contrained","Linear Fit"])
grid(ax4, 'on');
