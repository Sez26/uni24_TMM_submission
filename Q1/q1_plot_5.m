% visualising gravity model fitting
% Create a tiled layout for a 2x2 grid
t = tiledlayout(2, 2, 'TileSpacing', 'Compact', 'Padding', 'Compact');

% Title for the entire layout
title(t, 'MSOA Gravity Model', 'FontSize', 14, 'FontWeight', 'bold');

% First subplot
ax1 = nexttile;
% for MSOA plotting scatter every 100 values
smp_int = 1000;
scatter(MSOA_x(1:smp_int:end), MSOA_y(1:smp_int:end), 'DisplayName', 'MSOA data')
hold on
% plotting fitted model
lin_lab = sprintf("Linear model: alpha = %.2f, c = %.2e.", MSOA_alpha, MSOA_c);
plot(MSOA_x, MSOA_fit.Fitted,'r-', 'LineWidth', 2, 'DisplayName', lin_lab)
title(ax1, 'Fitting Linear Model', 'Interpreter','latex');
xlabel(ax1, '$\log(d_{ij})$', 'Interpreter','latex');
ylabel(ax1, '$\log((T_{ij})/(O_i D_j))$', 'Interpreter','latex');
legend;
grid(ax1, 'on');

% residuals
ax2 = nexttile;
scatter(ax2, 1:smp_int:numel(MSOA_res), MSOA_res(1:smp_int:end));
title(ax2, 'Residuals', 'Interpreter','latex');
xlabel(ax2, 'Indices', 'Interpreter','latex');
ylabel(ax2, 'Residuals', 'Interpreter','latex');
grid(ax2, 'on');

% exclude diagonals
% Get the size of the matrix
[m, n] = size(MSOA_res);
% Create a logical mask for the diagonal elements
diagMask = eye(m, n);
% Create a logical mask for all elements (complement of the diagonal)
nonDiagMask = ~diagMask;
lin_non_diag_idx = find(nonDiagMask);
ax3 = nexttile;
scatter(ax3, lin_non_diag_idx(1:smp_int:end), MSOA_res(lin_non_diag_idx(1:smp_int:end)));
title(ax3, 'Residuals - No Domestic Journeys', 'Interpreter','latex');
xlabel(ax3, 'Indices', 'Interpreter','latex');
ylabel(ax3, 'Residuals', 'Interpreter','latex');
grid(ax3, 'on');