# Makefile for source rpm: nut
# $Id$
NAME := nut
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
