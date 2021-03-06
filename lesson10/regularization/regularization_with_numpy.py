#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Authors: xiake(kedou1993@163.com)
Date:    2017/11/29
"""

import matplotlib.pyplot as plt
import utils

# 绘图相关设置
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'


def model(X, Y, model_name="_without_regularization",
          learning_rate=0.3, iteration_num=30000, print_cost=True,
          lambd=0, keep_prob=1):
    """
    实现一个3层神经网络：三层网络的激活函数分别为RELU，RELU，SIGMOID
    Args:
        X: 输入数据，尺寸大小为(输入尺寸, 样本数量)
        Y: 数据真实标签，1表示蓝点，0表示红点，尺寸大小为(输出尺寸, 样本数量)
        model_name: model的名字，用于绘图输出，例如可用”_without_regularization“表示模型不采用任何正则化方式
        learning_rate: 学习步长
        iteration_num: 迭代次数
        print_cost: 打印flag，如果为真，则每10000次迭代输出一个目标函数cost值
        lambd: L2正则化超参数
        keep_prob: dropout操作超参数，取值范围为(0,1]，表示在dropout过程中一个神经元保持激活的概率
    Return:
        parameters: 模型的参数，可用于预测
    """


    m = X.shape[1]  # 样本数量
    layers_dims = [X.shape[0], 20, 3, 1]
    gradients = {}
    costs = []  # 用于记录cost值

    # 初始化参数
    parameters = utils.initialize(layers_dims)

    # 梯度下降循环

    for i in range(0, iteration_num):

        # 正向传播
        # 不使用dropout
        if keep_prob == 1:
            a3, cache = utils.forward_calculate(X, parameters)
        # 使用dropout
        elif keep_prob < 1:
            a3, cache = utils.forward_calculate_with_dropout(
                X, parameters, keep_prob)

        # 计算目标函数cost值
        # 不使用L2正则化
        if lambd == 0:
            cost = utils.calculate_cost(a3, Y)
        # 使用L2正则化
        else:
            cost = utils.calculate_cost_with_regularization(
                a3, Y, parameters, lambd)

        assert (lambd == 0 or keep_prob == 1)
        # 实际操作中允许同时使用L2正则化和dropot，但在本实验中每次仅使用其中一种正则化方法

        # 反向传播
        # 不使用正则化
        if lambd == 0 and keep_prob == 1:
            gradients = utils.backward_calculate(X, Y, cache)
        # 使用L2正则化
        elif lambd != 0:
            gradients = utils.backward_calculate_with_regularization(
                X, Y, cache, lambd)
        # 使用dropout
        elif keep_prob < 1:
            gradients = utils.backward_calculate_with_dropout(
                X, Y, cache, keep_prob)

        # 更新参数
        parameters = utils.update(
            parameters, gradients, learning_rate)

        # 如果绘图标志位print_cost为真，则每10000次迭代输出一个目标函数cost值
        if print_cost and i % 10000 == 0:
            print "Cost after iteration {}: {}".format(i, cost)
        if print_cost and i % 1000 == 0:
            costs.append(cost)

    # 绘制目标函数cost曲线
    plt.clf()
    plt.plot(costs)
    plt.ylabel('cost')
    plt.xlabel('iterations (x1,000)')
    plt.title("Learning rate =" + str(learning_rate))
    plt.savefig("cost" + model_name + ".png")

    return parameters


def main():
    """
    分别训练不使用正则化的原始模型、使用L2正则化的模型、使用dropout的模型，输出cost值、预测准确率、边界预测结果等信息

    """

    # 读入数据集
    train_X, train_Y, test_X, test_Y = utils.load_dataset("data")

    # 训练不使用正则化的原始模型
    model_name = "_without_regularization"
    parameters = model(train_X, train_Y, model_name)
    # 在训练集和测试集上的进行预测并输出准确率
    print "On the training set:"
    predictions_train = utils.predict(train_X, train_Y, parameters)
    print "On the test set:"
    predictions_test = utils.predict(test_X, test_Y, parameters)
    # 绘制边界预测结果图
    plt.clf()
    plt.title("Model without regularization")
    axes = plt.gca()
    axes.set_xlim([-0.75, 0.40])
    axes.set_ylim([-0.75, 0.65])
    utils.plot_boundary(
        lambda x: utils.predict_decision(parameters, x.T), train_X, train_Y,
        "decision_boundary" + model_name + ".png")

    # 训练使用L2正则化的模型
    model_name = "_with_L2-regularization"
    parameters = model(train_X, train_Y, model_name, lambd=0.7)
    # 在训练集和测试集上的进行预测并输出准确率
    print "On the train set:"
    predictions_train = utils.predict(train_X, train_Y, parameters)
    print "On the test set:"
    predictions_test = utils.predict(test_X, test_Y, parameters)
    # 绘制边界预测结果图
    plt.clf()
    plt.title("Model with L2-regularization")
    axes = plt.gca()
    axes.set_xlim([-0.75, 0.40])
    axes.set_ylim([-0.75, 0.65])
    utils.plot_boundary(
        lambda x: utils.predict_decision(parameters, x.T), train_X, train_Y,
        "decision_boundary" + model_name + ".png")

    # 训练使用dropout的模型
    model_name = "_with_dropout"
    parameters = model(train_X, train_Y, model_name, keep_prob=0.86)
    # 在训练集和测试集上的进行预测并输出准确率
    print "On the train set:"
    predictions_train = utils.predict(train_X, train_Y, parameters)
    print "On the test set:"
    predictions_test = utils.predict(test_X, test_Y, parameters)
    # 绘制边界预测结果图
    plt.clf()
    plt.title("Model with dropout")
    axes = plt.gca()
    axes.set_xlim([-0.75, 0.40])
    axes.set_ylim([-0.75, 0.65])
    utils.plot_boundary(
        lambda x: utils.predict_decision(parameters, x.T), train_X, train_Y,
        "decision_boundary" + model_name + ".png")


if __name__ == "__main__":
    main()
