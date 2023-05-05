#!/bin/sh
cd $(dirname $(dirname $(readlink -f "$0"))..)

export FLASK_APP=auth.app

flask admin create $1 $2 $3

