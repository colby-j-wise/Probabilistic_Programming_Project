import edward as ed
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns


def critique_glm(posterior_pred, x, x_test, y_test, w, b, qw, qb):

    def t_max(data_dict, latent):
        return tf.reduce_max(data_dict[posterior_pred])

    def t_min(data_dict, latent):
        return tf.reduce_min(data_dict[posterior_pred])

    def t_mean(data_dict, latent):
        return tf.reduce_mean(data_dict[posterior_pred])

    ppc_1 = ed.ppc(t_max,
                   data={
                       x: x_test.as_matrix(),
                       posterior_pred: np.reshape(y_test.as_matrix(),
                                                  (y_test.shape[0]))
                   },
                   latent_vars={w: qw, b: qb})
    ed.ppc_stat_hist_plot(ppc_1[1][1], ppc_1[0], stat_name=r'$T \equiv max$',
                          bins=10)
    plt.show()
    ppc_2 = ed.ppc(t_min,
                   data={
                       x: x_test.as_matrix(),
                       posterior_pred: np.reshape(y_test.as_matrix(),
                                                  (y_test.shape[0]))
                   },
                   latent_vars={w: qw, b: qb})
    ed.ppc_stat_hist_plot(ppc_2[1][1], ppc_1[0], stat_name=r'$T \equiv min$',
                          bins=10)
    plt.show()
    ppc_3 = ed.ppc(t_mean,
                   data={
                       x: x_test.as_matrix(),
                       posterior_pred: np.reshape(y_test.as_matrix(),
                                                  (y_test.shape[0]))
                   },
                   latent_vars={w: qw, b: qb})
    ed.ppc_stat_hist_plot(ppc_3[1][1], ppc_1[0], stat_name=r'$T \equiv mean$',
                          bins=10)
    plt.show()


def min_max_gp_ppc(posterior_predictive, true_y, n_samples=100):
        with tf.Session() as sess:
            samples = posterior_predictive.sample([n_samples])
            mins = tf.reduce_min(samples, axis=1).eval(session=sess)
            maxes = tf.reduce_max(samples, axis=1).eval(session=sess)
            means = tf.reduce_mean(samples, axis=1).eval(session=sess)

        ax = sns.distplot(mins, kde=False)
        max_val = ax.get_ylim()[1]
        plt.vlines([min(true_y)], ymin=0.0, ymax=max_val)
        plt.show()

        ax = sns.distplot(maxes, kde=False)
        max_val = ax.get_ylim()[1]
        plt.vlines(max(true_y), ymin=0.0, ymax=max_val)
        plt.show()
