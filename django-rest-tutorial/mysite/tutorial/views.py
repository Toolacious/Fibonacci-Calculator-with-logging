from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

import os
import os.path as osp
import sys
import json 
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../../build/service/")
sys.path.insert(0, BUILD_DIR)
import fib_pb2_grpc
import fib_pb2
import grpc
import log_pb2
import log_pb2_grpc

import paho.mqtt.client as mqtt
# Create your views here.


class EchoView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        return Response(data={'echo': 'hello world'}, status=200)


class FibonacciView(APIView):
    permission_classes = (permissions.AllowAny,)

    def __init__(self):

        mqttHost = "localhost"
        mqttPort = 1883
        self.client = mqtt.Client()
        self.client.connect(host=mqttHost, port=mqttPort)

    def get(self, request):
        host = "localhost:8088"
        with grpc.insecure_channel(host) as channel:
            stub = log_pb2_grpc.FibCalculatorLogStub(channel)

            request = log_pb2.LogRequest()
            response = stub.getHistory(request)
            resHistory = []
            for idx, history in enumerate(response.value):
                history = json.loads(history);
                history['id'] = idx
                resHistory.append(history)
            return Response({"history": resHistory}, status=200)

    def post(self, request):
        host = "localhost:8080"
        fiborder = request.data.get('order')
        with grpc.insecure_channel(host) as channel:
            stub = fib_pb2_grpc.FibCalculatorStub(channel)

            request = fib_pb2.FibRequest()
            request.order = fiborder

            response = stub.Compute(request)
            resDict = {'order': fiborder, 'value': response.value}
            payload = json.dumps(resDict)
            self.client.publish(topic='log', payload=payload)
            return Response(data=resDict, status=200)
