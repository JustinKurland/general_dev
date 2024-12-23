# Define the full parameter space for SplineCalib
reg_params = np.logspace(-4, 2, 10)  # Regularization parameters
logodds_eps_values = [1e-7, 1e-5, 1e-3]  # Log-odds epsilon values
knot_sample_sizes = [10, 20, 30, 40, 50]  # Number of knots to sample
unity_prior_weights = [None, 10, 25, 50, 75, 100]  # Unity prior weights
reg_prec_values = [3, 4, 5, 6]  # Precision for choosing the best regularization parameter
force_knot_endpts_values = [True, False]  # Force inclusion of end points as knots
add_knots_values = [None, np.linspace(0, 1, 20), np.array([0.05, 0.95])]  # Specific knots
max_iter_values = [1000, 2000, 5000]  # Max iterations for logistic regression
log_scale_values = [True, False]  # Use log scale for transformations

# Combine all parameters into a grid
spline_parameter_grid = list(
    product(
        reg_params,
        logodds_eps_values,
        knot_sample_sizes,
        unity_prior_weights,
        reg_prec_values,
        force_knot_endpts_values,
        add_knots_values,
        max_iter_values,
        log_scale_values,
    )
)


from sklearn.metrics import log_loss
import ml_insights as mli

# Placeholder for calibration results
calibration_results = []

# Loop through the parameter grid
for config in spline_parameter_grid:
    (
        reg_param,
        logodds_eps,
        knot_sample_size,
        unity_prior_weight,
        reg_prec,
        force_knot_endpts,
        add_knots,
        max_iter,
        log_scale,
    ) = config

    # Initialize SplineCalib with the current configuration
    sc = mli.SplineCalib(
        reg_param_vec=np.logspace(-4, 4, 50),
        logodds_eps=logodds_eps,
        knot_sample_size=knot_sample_size,
        unity_prior_weight=unity_prior_weight,
        reg_prec=reg_prec,
        force_knot_endpts=force_knot_endpts,
        add_knots=add_knots,
        max_iter=max_iter,
        log_scale=log_scale,
    )

    # Fit the calibrator
    try:
        sc.fit(oof_probs, y_train)

        # Calibrate test set probabilities
        y_test_pred_spline = sc.calibrate(y_test_pred_uncalib)

        # Compute log-loss for this configuration
        spline_log_loss = log_loss(y_test, y_test_pred_spline)

        # Save results
        calibration_results.append(
            {
                "Configuration": config,
                "Log-Loss": spline_log_loss,
            }
        )
    except Exception as e:
        print(f"Error with configuration {config}: {e}")
        continue

# Sort results by log-loss
calibration_results = sorted(calibration_results, key=lambda x: x["Log-Loss"])

# Display the best result
best_result = calibration_results[0]
print("Best Spline Calibration Configuration:", best_result)
