% Show spatial networks with a Pos_table = [Lon,Lat] and an adjacency matrix A
function plot_network(A,pos_table,s)

N = size(A,2); 

geolimits([min(pos_table(:,1)) max(pos_table(:,1))],[min(pos_table(:,2)) max(pos_table(:,2))])
hold on;

for i = 1 : N
    for j = i+1 : N
        if A(i,j) == 1
            xx = pos_table([i,j],1)';
            yy = pos_table([i,j],2)';
            hold on;
            % geoplot(xx,yy,s,'linewidth',0.5,'MarkerSize',,'MarkerEdgeColor','w','MarkerFaceColor',[0,1,0]);
            geoplot(xx,yy,s,'linewidth',1);
        end
    end
end
geobasemap streets;