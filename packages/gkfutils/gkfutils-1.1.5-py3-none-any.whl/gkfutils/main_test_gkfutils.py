import gkfutils

if __name__ == '__main__':
    print(gkfutils.__version__)
    # gkfutils.rename_files(data_path="E:\\Gosuncn\\Projects\\006.Fire_Smoke_Det\\SSOD_test\\unlabel_pred_same", use_orig_name=False, new_name_prefix="Test", zeros_num=20, start_num=0)
    # gkfutils.save_file_path_to_txt(data_path="E:\\Gosuncn\\Projects\\006.Fire_Smoke_Det\\SSOD_test\\unlabel_pred_same", abspath=True)


    # gkfutils.cv.utils.extract_one_gif_frames(gif_path="")
    # gkfutils.cv.utils.extract_one_video_frames(video_path="", gap=5)
    # gkfutils.cv.utils.extract_videos_frames(base_path="", gap=5, save_path="")

    # gkfutils.utils.split_dir_multithread(data_path="", split_n=10)
    # gkfutils.utils.split_dir_by_file_suffix(data_path="")

    # gkfutils.utils.random_select_files(data_path="", select_num=500, move_or_copy="copy", select_mode=0)
    # gkfutils.cv.utils.random_select_images_and_labels(data_path="", select_num=500, move_or_copy="copy", select_mode=0)

    # gkfutils.cv.utils.labelbee2yolo(data_path="", copy_image=True)
    # gkfutils.cv.utils.yolo2labelbee(data_path="")
    # gkfutils.cv.utils.voc2yolo(data_path="", classes=['dog', ], val_percent=0.1)
    # # gkfutils.cv.utils.yolo2voc(data_path="")  # TODO
    # gkfutils.cv.utils.labelbee_kpt_to_yolo(data_path="", copy_image=False)
    # gkfutils.cv.utils.labelbee_kpt_to_dbnet(data_path="", copy_image=True)
    # gkfutils.cv.utils.labelbee_seg_to_png(data_path="")
    # gkfutils.cv.utils.coco2yolo(root="")
    # # gkfutils.cv.utils.yolo2coco(root="")  # TODO
    # gkfutils.cv.utils.labelbee_kpt_to_labelme_kpt(data_path="")
    # gkfutils.cv.utils.labelbee_kpt_to_labelme_kpt_multi_points(data_path="")

    # gkfutils.cv.utils.convert_Stanford_Dogs_Dataset_annotations_to_yolo_format(data_path="")
    # gkfutils.cv.utils.convert_WiderPerson_Dataset_annotations_to_yolo_format(data_path="")
    # gkfutils.cv.utils.convert_TinyPerson_Dataset_annotations_to_yolo_format(data_path="")
    # gkfutils.cv.utils.convert_AI_TOD_Dataset_to_yolo_format(data_path="")

    # gkfutils.cv.utils.vis_yolo_label(data_path="", print_flag=False, color_num=1000, rm_small_object=False, rm_size=32)  # TODO: 1.rm_small_object have bugs.
    # gkfutils.cv.utils.list_yolo_labels(label_path="")
    # gkfutils.cv.utils.change_txt_content(txt_base_path="")
    # gkfutils.cv.utils.remove_yolo_txt_contain_specific_class(data_path="", rm_cls=(0, ))
    # gkfutils.cv.utils.remove_yolo_txt_small_bbx(data_path="", rm_cls=(0, ), rmsz=(48, 48))
    # gkfutils.cv.utils.select_yolo_txt_contain_specific_class(data_path="", select_cls=(3, ))
    # gkfutils.cv.utils.merge_txt(path1="", path2="")
    # gkfutils.cv.utils.merge_txt_files(data_path="")


    # gkfutils.cv.utils.dbnet_aug_data(data_path="", bg_path="", maxnum=10000)
    # gkfutils.cv.utils.vis_dbnet_gt(data_path="")
    # gkfutils.cv.utils.warpPerspective_img_via_labelbee_kpt_json(data_path="")

    # alpha = ' ' + '0123456789' + '.:/\\-' + 'ABbC'
    # alpha = gkfutils.cv.utils.read_ocr_lables(lbl_path="")
    # gkfutils.cv.utils.ocr_data_gen_train_txt_v2(data_path="", LABEL=alpha)
    # gkfutils.cv.utils.check_ocr_label(data_path="", label=alpha)
    # gkfutils.cv.utils.random_select_files_according_txt(data_path="", select_percent=0.25)

    # gkfutils.cv.utils.crnn_data_makeBorder(data_path="")
    # gkfutils.cv.utils.do_makeBorderv6(data_path="")

    # gkfutils.cv.utils.ocr_data_gen_train_txt(data_path="", LABEL=alpha)
    # gkfutils.cv.utils.ocr_data_gen_train_txt_v2(data_path="", LABEL=alpha)
    # gkfutils.cv.utils.ocr_data_merge_train_txt_files_v2(data_path="", LABEL=alpha)
    # gkfutils.cv.utils.check_ocr_label(data_path="", label=alpha)
    # gkfutils.cv.utils.random_select_files_according_txt(data_path="", select_percent=0.25)
    # gkfutils.cv.utils.random_select_files_from_txt(data_path="", n=2500)
    # gkfutils.cv.utils.convert_text_renderer_json_to_my_dataset_format(data_path="")
    # gkfutils.cv.utils.convert_Synthetic_Chinese_String_Dataset_labels(data_path="")
    # gkfutils.cv.utils.convert_to_ocr_rec_data_mtwi(data_path="")
    # gkfutils.cv.utils.convert_to_ocr_rec_data_ShopSign1(data_path="")
    # gkfutils.cv.utils.convert_to_ocr_rec_data_ShopSign2(data_path="")
    # gkfutils.cv.utils.ocr_train_txt_change_to_abs_path()
    # gkfutils.cv.utils.get_ocr_train_txt_alpha(data_path="")
    # gkfutils.cv.utils.check_ocr_train_txt(data_path="")
    # gkfutils.cv.utils.random_select_images_from_ocr_train_txt(data_path="", select_num= 5000)
    # gkfutils.cv.utils.ocr_train_txt_split_to_train_and_test(data_path="", train_percent=0.8)

    # gkfutils.cv.utils.convert_to_jpg_format(data_path="")
    # gkfutils.cv.utils.convert_to_png_format(data_path="")
    # gkfutils.cv.utils.convert_to_gray_image(data_path="")
    # gkfutils.cv.utils.convert_to_binary_image(data_path="", thr_low=88)
    # gkfutils.cv.utils.crop_image_according_labelbee_json(data_path="", crop_ratio=(1, 1.2, 1.5, ))
    # gkfutils.cv.utils.crop_ocr_rec_img_according_labelbee_det_json(data_path="")
    # gkfutils.cv.utils.crop_image_according_yolo_txt(data_path="", CLS=(0, ), crop_ratio=(1.0, ))  # 1.0, 1.1, 1.2, 1.5, 2.0, 2.5, 3.0
    # gkfutils.cv.utils.random_crop_gen_cls_negative_samples(data_path="", random_size=(196, 224, 256, 288, 384), randint_low=1, randint_high=4, hw_dis=100, dst_num=1000)
    # gkfutils.cv.utils.seg_object_from_mask(base_path="")






