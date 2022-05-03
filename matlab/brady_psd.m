clear all;

%%
%Figure/Proc Commands Params

WIN = 10;
CORRECTION_FACTOR = 1;
N = 10;

%ONLY ONE SHOULD BE ENABLED AT A TIME
MANUAL = 1;
PLOMB = 0;
PWELCH = 0;

figure(1);

set(gca,'fontname', 'serif');
set(gca,'FontSize',7)

set(gcf, 'PaperUnits', 'inches');
x_width=7.6 ;y_width=8
set(gcf, 'PaperPosition', [0 0 x_width y_width]); %

noisexxx = 0;
noiseyyy = 0;
noisezzz = 0;
%%
%Data manipulation and plotting for PSD

SENSORS = 4;
OVERSAMPLING = 1;

%check for bad input params
if xor(xor(PWELCH, PLOMB), MANUAL) == 0
    disp("BAD INPUT PARAMS, ONLY ONE METHOD SHOULD BE SELECTED FOR PSD");
    return;
end

for(ii = 1:N) 
    
    %Data retrieval
    FILE = strcat('./data/03-15-2022/noise_floor', int2str(ii-1));
    FILE = strcat(FILE, '.txt');
    %FILE = "./data/03-15-2022/1319xxxx_all100hours1_processed_data_fixed.txt";
    %FILE = "./data/03-15-2022/1319xxxx_all10sec_processed_data.txt";

    [b, PERIOD, txx] = getdata_quad(FILE, OVERSAMPLING, SENSORS, true, false);
    
    delete_arr = [];
    
    for(kj = (1:length(txx)-1))
        if(txx(kj) > txx(kj+1)) 
            delete_arr = [delete_arr, kj];
        end;
    end;
    
    len = length(b{1}(:,1));

    bxx = zeros(len, 1);
    byy = zeros(len, 1);
    bzz = zeros(len, 1);

    if(SENSORS == 4)
        for(jj = 1: SENSORS)
            bxx = bxx + b{jj}(:, 1);
            byy = byy + b{jj}(:, 2);
            bzz = bzz + b{jj}(:, 3);
        end;
        bxx = bxx./4.0;
        byy = byy./4.0;
        bzz = bzz./4.0;

    end;
    
    %Calculating PSD via different methods
    
    txx(delete_arr) = [];
    bxx(delete_arr) = [];
    byy(delete_arr) = [];
    bzz(delete_arr) = [];
    
    %x-axis calulation and plotting

    [psd_swrt_hz, F] = pwelch(bxx, [], [], [], 1 / PERIOD); %using pwelch method
    
    if PLOMB
        [psd_swrt_hz, F] = plomb(bxx,txx); %using plomb library
    end
    
    if CORRECTION_FACTOR
        psd_swrt_hz = psd_swrt_hz ./ length(bxx);
    end 
        
    psd_swrt_hz = psd_swrt_hz.^.5;
    
    %manually doing it via fft of autocorellation function
    
    if MANUAL 
        lens = length(bxx);
        xat = autocorr(bxx,'NumLags',lens-1); %autocorrelation of signal with itself 
        Yat = fft(xat); %fft of autocorrellation function yields psd
        P2 = abs(Yat);
        if CORRECTION_FACTOR
            P2 = abs(Yat/lens); %matlab fft does not take into account 1/N correction factor...do it here
        end
        psd_swrt_hz = P2(1:lens/2+1); %compute the single sided amplitude spectrum
        psd_swrt_hz(2:end-1) = 2*psd_swrt_hz(2:end-1); 
        psd_swrt_hz = psd_swrt_hz.^.5;
        F = (1 / PERIOD)*(0:(lens/2))/lens; %generate frequency domain vector
    end
    
    %determine the noise of window ~1hz defined by index width (fix-WIN)
    tempf = abs(F - 1);
    [tadata, fix] = min( tempf );
    noise = mean(psd_swrt_hz(fix - WIN:fix + WIN));
    
    noisexxx = noisexxx + noise;
    
    psd_swrt_hz = psd_swrt_hz * 1E3;
    
    %plotting for x-axis
    subplot(3,1,1);
    hold on;
    semilogy(F,psd_swrt_hz, 'LineWidth',2);grid on;
    ylabel('\textbf{PSD B$_x$ $(\frac{pT}{\sqrt{Hz}}$)}', 'interpreter','latex');
    xlabel('\textbf{Freq (Hz)}', 'interpreter','latex');
    xlim([1E-3 1E2])
    ylim([1 1E2])
    set(gca,'XScale','log');
    set(gca,'YScale','log');
    
    %same as before but for y-axis

    [psd_swrt_hz, F] = pwelch(byy, [], [], [], 1 / PERIOD);
    
    if PLOMB
        [psd_swrt_hz, F] = plomb(byy,txx);
    end
    
    if CORRECTION_FACTOR
        psd_swrt_hz = psd_swrt_hz ./ length(byy);
    end
    
    psd_swrt_hz = psd_swrt_hz.^.5;
    
    %manually doing it via fft of autocorellation function
    
    if MANUAL
        lens = length(byy);
        xat = autocorr(byy,'NumLags',lens-1); %autocorrelation of signal with itself
        Yat = fft(xat); %fft of autocorrellation function yields psd
        P2 = abs(Yat);
        if CORRECTION_FACTOR
            P2 = abs(Yat/lens); %matlab fft does not take into account 1/N correction factor...do it here
        end
        psd_swrt_hz = P2(1:lens/2+1); %compute the single sided amplitude spectrum
        psd_swrt_hz(2:end-1) = 2*psd_swrt_hz(2:end-1); 
        psd_swrt_hz = psd_swrt_hz.^.5;
        F = (1 / PERIOD)*(0:(lens/2))/lens; %generate frequency domain vector
    end
    
    tempf = abs(F - 1);
    [tadata, fix] = min( tempf );
    noise = mean(psd_swrt_hz(fix - WIN:fix + WIN));
    
    noiseyyy = noiseyyy + noise;
    
    psd_swrt_hz = psd_swrt_hz * 1E3;

    subplot(3,1,2);
    hold on;
    semilogy(F,psd_swrt_hz, 'LineWidth',2);grid on;
    ylabel('\textbf{PSD B$_y$ $(\frac{pT}{\sqrt{Hz}}$)}', 'interpreter','latex');
    xlabel('\textbf{Freq (Hz)}', 'interpreter','latex');
    xlim([1E-3 1E2])
    ylim([1 1E2])
    set(gca,'XScale','log');
    set(gca,'YScale','log');
    
    
    %same as before but for z-axis

    [psd_swrt_hz, F] = pwelch(bzz, [], [], [], 1 / PERIOD);

    if PLOMB
        [psd_swrt_hz, F] = plomb(bzz,txx);
    end
    
    if CORRECTION_FACTOR
        psd_swrt_hz = psd_swrt_hz ./ length(bzz);
    end
    
    psd_swrt_hz = psd_swrt_hz.^.5;
    
    if MANUAL
        lens = length(bzz);
        xat = autocorr(bzz,'NumLags',lens-1); %autocorrelation of signal with itself
        Yat = fft(xat); %fft of autocorrellation function yields psd
        P2 = abs(Yat);
        if CORRECTION_FACTOR
            P2 = abs(Yat/lens); %matlab fft does not take into account 1/N correction factor...do it here
        end
        psd_swrt_hz = P2(1:lens/2+1); %compute the single sided amplitude spectrum
        psd_swrt_hz(2:end-1) = 2*psd_swrt_hz(2:end-1); 
        psd_swrt_hz = psd_swrt_hz.^.5;
        F = (1 / PERIOD)*(0:(lens/2))/lens; %generate frequency domain vector
    end
    
    tempf = abs(F - 1);
    [tadata, fix] = min( tempf );
    noise = mean(psd_swrt_hz(fix - WIN:fix + WIN));
    
    noisezzz = noisezzz + noise;
    
    psd_swrt_hz = psd_swrt_hz * 1E3;

    subplot(3,1,3);
    hold on;
    semilogy(F,psd_swrt_hz, 'LineWidth',2);grid on;
    ylabel('\textbf{PSD B$_z$ $(\frac{pT}{\sqrt{Hz}}$)}', 'interpreter','latex');
    xlabel('\textbf{Freq (Hz)}', 'interpreter','latex');
    xlim([1E-3 1E2])
    ylim([1 1E2])
    set(gca,'XScale','log');
    set(gca,'YScale','log');
end;

%%
%Final calculations and saving the figure

%average the noise across all 10 tests
noisexxx = noisexxx ./ N .* 1E3
noiseyyy = noiseyyy ./ N .* 1E3
noisezzz = noisezzz ./ N .* 1E3
noisexxx = round(noisexxx,3);
noiseyyy = round(noiseyyy,3);
noisezzz = round(noisezzz,3);

%noise density in figures at 1hz and add vertical line at 1hz
subplot(3,1,1);
hold on;
xline(1, '--k','LineWidth',2);
title(strcat(strcat('\textbf{NOISE DENSITY @1$Hz$ $\Rightarrow$  ', num2str(noisexxx)), ' $(\frac{pT}{\sqrt{Hz}}$)}'),'interpreter','latex', 'FontSize',12);

subplot(3,1,2);
hold on;
xline(1, '--k','LineWidth',2);
title(strcat(strcat('\textbf{NOISE DENSITY @1$Hz$ $\Rightarrow$  ', num2str(noiseyyy)), ' $(\frac{pT}{\sqrt{Hz}}$)}'),'interpreter','latex', 'FontSize',12);

subplot(3,1,3);
hold on;
xline(1, '--k','LineWidth',2);
title(strcat(strcat('\textbf{NOISE DENSITY @1$Hz$ $\Rightarrow$ ', num2str(noisezzz)), ' $(\frac{pT}{\sqrt{Hz}}$)}'),'interpreter','latex', 'FontSize',12);

if PWELCH
    print -dpng noise_floor_quad_pwelch
    %print -dpng noise_floor_quad_pwelch_short
    %print -dpng noise_floor_quad_pwelch_long
end

if PLOMB
    print -dpng noise_floor_quad_plomb
end

if MANUAL 
    %print -dpng noise_floor_quad_manual_short_no_scaling
    %print -dpng noise_floor_quad_manual_long_no_scaling
    print -dpng noise_floor_quad_manual
end


