%% Plotting the grids (Quadtree from Basilisk C dump files)
% Author: Vatsal Sanjay
% vatsalsanjay@gmail.com
% Physics of Fluids
clc
clear
close
%% Output Folder
folder = 'Grids'; % output folder
opFolder = fullfile(cd, folder);
if ~exist(opFolder, 'dir')
mkdir(opFolder);
end
%%
tic
nGFS = 99;
dt = 0.01;
xmin = 0.0; xmin1 = 0.0;
xmax = 1.0; xmax1 = 0.12;
ymin = 0.0; ymin1 = 0.0;
ymax = 1.0; ymax1 = 0.12;
LEVEL = 9;
Xg = {[]};
Xf = {[]};
for ti = 1:1:nGFS
    tic
    t = ti*dt;
    filename = sprintf('intermediate/snapshot-%5.4f',t);
    
    % Grids
    ll=evalc(sprintf('!./getCells %s', filename));
    bolo=textscan(ll,'%f %f\n');
    Xg{ti}.x = bolo{1}; Xg{ti}.y = bolo{2};
    Xg{ti}.x = reshape(Xg{ti}.x, [5, int16(length(Xg{ti}.x)/5)]);
    Xg{ti}.y = reshape(Xg{ti}.y, [5, int16(length(Xg{ti}.y)/5)]);
    % Facets
    ll=evalc(sprintf('!./getFacet %s', filename));
    bolo=textscan(ll,'%f %f\n');
    Xf{ti}.x = bolo{1}; Xf{ti}.y = bolo{2};
    Xf{ti}.x = reshape(Xf{ti}.x, [2, int16(length(Xf{ti}.x)/2)]);
    Xf{ti}.y = reshape(Xf{ti}.y, [2, int16(length(Xf{ti}.y)/2)]);
    
    % plotting
    figure1 = figure('visible','off','WindowState','fullscreen','Color',[1 1 1]);
    axes1 = axes('Parent',figure1);
    hold(axes1,'on');
    name = [folder '/' sprintf('grid%4.4d.png',ti)];
    plot(Xg{ti}.x, Xg{ti}.y,'-','color',[0.5 0.5 0.5],'MarkerSize',30,'LineWidth',1);
    plot(Xf{ti}.x, Xf{ti}.y,'-','color',[0.0 0.0 0.0],'MarkerSize',30,'LineWidth',3);
%     box(axes1,'on');
%     set(axes1,'FontName','times new roman','FontSize',30,'FontWeight','bold',...
%         'LineWidth',3);
%     xlabel('\boldmath{$X$}','LineWidth',2,'FontWeight','bold','FontSize',50,...
%                 'FontName','times new roman',...
%                 'Interpreter','latex');
%     ylabel('\boldmath{$Y$}','LineWidth',2,'FontWeight','bold','FontSize',50,...
%         'FontName','times new roman',...
%         'Interpreter','latex'); 
    axis square
%     xlim([xmin xmax])
%     ylim([ymin ymax])
    xlim([xmin1 xmax1]);
    ylim([ymin1 ymax1]);
    axis off;
    set(figure1,'pos',[1 1 480 480]);
    print(name,'-dpng','-r300')
    close all;
    fprintf('%d of %d\n',ti, nGFS);
    toc
end
%% Saving the data
save('grids','Xg','Xf','-v7.3');
toc
