function [x_UE, f_UE, ef_UE, x_SO, f_SO, ef_SO, PoA] = Price_of_Anarchy(H, f, A, bvec, Aeq, beq, LB, UB)
    [x_UE,~,ef_UE]=quadprog(H, f, A, bvec, Aeq, beq, LB, UB);
    [x_SO,f_SO,ef_SO]=quadprog(2*H, f, A, bvec, Aeq, beq, LB, UB);
    f_UE = f'*x_UE + x_UE'*H*x_UE;
    % f_SO = avec'*x_SO + x_SO'*H*x_SO;
    PoA = f_UE/f_SO;
    if isnan(PoA)
        PoA = 1; % PoA tends to 1 when d is very small
    end
end