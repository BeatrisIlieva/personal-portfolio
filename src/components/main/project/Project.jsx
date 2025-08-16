import { Video } from './video/Video';
import styles from './Project.module.scss';
import { mediaConfig } from './config';
import { Image } from './image/Image';

export const Project = () => {
    return (
        <section id='project' className={styles['project']}>
            <Image imageName='home.png' />
            <Video
                videoName='product-list'
                text={mediaConfig['product-list']}
            />

            <Video videoName='add-to-bag' text={mediaConfig['add-to-bag']} />
            <Image imageName='product-item.png' />

            <Video videoName='register' text={mediaConfig['register']} rowAlignment='one-row'/>

            <Video videoName='product-review' text={mediaConfig['product-review']} />
            <Image imageName='wishlist.png' />

            <Video videoName='reset-password' text={mediaConfig['reset-password']} rowAlignment='one-row'/>
        </section>
    );
};
